"""Concurrent image downloading utilities."""
import asyncio
import logging
import os
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urlparse

import aiohttp
from PIL import Image
from io import BytesIO

from autopaper.utils.logging import get_logger
from autopaper.utils.profiling import profile

logger = get_logger(__name__)


async def download_single_image(
    session: aiohttp.ClientSession,
    url: str,
    output_path: Path,
    timeout: int = 30
) -> bool:
    """Download a single image asynchronously.

    Args:
        session: aiohttp ClientSession
        url: Image URL
        output_path: Path to save the image
        timeout: Download timeout in seconds

    Returns:
        True if successful, False otherwise
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
            response.raise_for_status()
            content = await response.read()

            # Save to file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(content)

            logger.debug(f"Downloaded image: {output_path.name}")
            return True

    except asyncio.TimeoutError:
        logger.warning(f"Timeout downloading image: {url}")
        return False
    except Exception as e:
        logger.warning(f"Error downloading image from {url}: {e}")
        return False


async def download_images_concurrent(
    image_urls: List[Tuple[str, Path]],
    max_concurrent: int = 5,
    timeout: int = 30
) -> Tuple[int, int]:
    """Download multiple images concurrently.

    Args:
        image_urls: List of (url, output_path) tuples
        max_concurrent: Maximum number of concurrent downloads
        timeout: Timeout for each download in seconds

    Returns:
        Tuple of (successful_count, failed_count)

    Examples:
        >>> urls = [
        ...     ("http://example.com/img1.jpg", Path("images/img1.jpg")),
        ...     ("http://example.com/img2.jpg", Path("images/img2.jpg")),
        ... ]
        >>> success, failed = await download_images_concurrent(urls, max_concurrent=3)
    """
    if not image_urls:
        return 0, 0

    # Create semaphore to limit concurrent downloads
    semaphore = asyncio.Semaphore(max_concurrent)

    async def download_with_semaphore(url: str, path: Path) -> bool:
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                return await download_single_image(session, url, path, timeout)

    # Create download tasks
    tasks = [
        download_with_semaphore(url, path)
        for url, path in image_urls
    ]

    # Execute all downloads concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Count successes and failures
    success_count = sum(1 for r in results if r is True)
    failed_count = len(results) - success_count

    logger.info(
        f"Downloaded {success_count}/{len(image_urls)} images "
        f"({failed_count} failed)"
    )

    return success_count, failed_count


def download_images_sync(
    image_urls: List[Tuple[str, Path]],
    timeout: int = 30
) -> Tuple[int, int]:
    """Synchronous wrapper for downloading images concurrently.

    Args:
        image_urls: List of (url, output_path) tuples
        timeout: Timeout for each download in seconds

    Returns:
        Tuple of (successful_count, failed_count)

    Examples:
        >>> urls = [
        ...     ("http://example.com/img1.jpg", Path("images/img1.jpg")),
        ... ]
        >>> success, failed = download_images_sync(urls)
    """
    try:
        # Get or create event loop
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()

        return loop.run_until_complete(
            download_images_concurrent(image_urls, timeout=timeout)
        )
    except Exception as e:
        logger.error(f"Error in concurrent download: {e}", exc_info=True)
        return 0, len(image_urls)


@profile(log_slow_calls=10.0)
def optimize_image(
    image_path: Path,
    max_size: int = 1200,
    quality: int = 85,
    convert_to_webp: bool = False
) -> Path:
    """Optimize image by resizing and compressing.

    Args:
        image_path: Path to input image
        max_size: Maximum width/height in pixels
        quality: JPEG/WebP quality (1-100)
        convert_to_webp: Convert to WebP format (smaller file size)

    Returns:
        Path to optimized image (may be same as input if optimization fails)

    Examples:
        >>> optimize_image(Path("large-image.jpg"))
        Path("large-image.jpg")  # Optimized in place

        >>> optimize_image(Path("image.jpg"), convert_to_webp=True)
        Path("image.webp")  # Converted to WebP
    """
    try:
        img = Image.open(image_path)

        # Calculate new dimensions
        width, height = img.size
        if max(width, height) > max_size:
            if width > height:
                new_width = max_size
                new_height = int(height * (max_size / width))
            else:
                new_height = max_size
                new_width = int(width * (max_size / height))

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.debug(f"Resized {image_path.name} to {new_width}x{new_height}")

        # Determine output format
        if convert_to_webp:
            output_path = image_path.with_suffix('.webp')
            img.save(output_path, 'WebP', quality=quality)

            # Remove original if different
            if output_path != image_path and image_path.exists():
                image_path.unlink()

            logger.debug(f"Converted to WebP: {output_path.name}")
            return output_path
        else:
            # Save in original format with optimization
            img.save(image_path, quality=quality, optimize=True)
            return image_path

    except Exception as e:
        logger.warning(f"Failed to optimize {image_path}: {e}")
        return image_path


def optimize_images_concurrent(
    image_paths: List[Path],
    max_size: int = 1200,
    quality: int = 85,
    convert_to_webp: bool = False
) -> int:
    """Optimize multiple images in sequence (PIL is not thread-safe).

    Args:
        image_paths: List of image paths to optimize
        max_size: Maximum width/height in pixels
        quality: JPEG/WebP quality (1-100)
        convert_to_webp: Convert to WebP format

    Returns:
        Number of successfully optimized images
    """
    success_count = 0

    for img_path in image_paths:
        try:
            optimize_image(img_path, max_size, quality, convert_to_webp)
            success_count += 1
        except Exception as e:
            logger.warning(f"Failed to optimize {img_path}: {e}")

    logger.info(f"Optimized {success_count}/{len(image_paths)} images")
    return success_count
