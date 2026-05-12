<?php

declare(strict_types=1);

namespace WebInsights;

use WebInsights\Storage\Storage;

final class Bootstrap
{
    public static function rootPath(): string
    {
        return dirname(__DIR__);
    }

    public static function storagePath(string $path = ''): string
    {
        $base = self::rootPath() . '/storage';
        return $path === '' ? $base : $base . '/' . ltrim($path, '/');
    }

    public static function fixturePath(string $path = ''): string
    {
        $base = self::rootPath() . '/fixtures';
        return $path === '' ? $base : $base . '/' . ltrim($path, '/');
    }

    public static function boot(): void
    {
        self::ensureDirectory(self::storagePath());
        self::ensureDirectory(self::storagePath('reports'));
    }

    public static function storage(): Storage
    {
        self::boot();
        return new Storage(self::storagePath('webinsights.sqlite'));
    }

    public static function ensureDirectory(string $path): void
    {
        if (!is_dir($path)) {
            mkdir($path, 0775, true);
        }
    }
}
