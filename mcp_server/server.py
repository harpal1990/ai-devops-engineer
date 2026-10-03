import os
import platform
import shutil
import subprocess

import psutil

from mcp.server.mcpserver import MCPServer


server = MCPServer("AI DevOps Tools")


@server.tool()
def get_system_info() -> dict:
    """Get basic Linux system information."""

    memory = psutil.virtual_memory()

    return {
        "hostname": platform.node(),
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "cpu_count": os.cpu_count(),
        "cpu_usage_percent": psutil.cpu_percent(interval=1),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_available_gb": round(memory.available / (1024**3), 2),
        "memory_usage_percent": memory.percent,
    }


@server.tool()
def get_disk_usage() -> dict:
    """Get disk usage for the root filesystem."""

    usage = shutil.disk_usage("/")

    total_gb = usage.total / (1024**3)
    used_gb = usage.used / (1024**3)
    free_gb = usage.free / (1024**3)

    return {
        "mount": "/",
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "used_percent": round(
            (usage.used / usage.total) * 100,
            2,
        ),
    }


@server.tool()
def get_top_processes() -> list:
    """Return the top 10 processes by CPU usage."""

    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "cpu_percent", "memory_percent"]
    ):
        try:
            info = process.info

            processes.append(
                {
                    "pid": info["pid"],
                    "name": info["name"],
                    "cpu_percent": info["cpu_percent"],
                    "memory_percent": round(
                        info["memory_percent"] or 0,
                        2,
                    ),
                }
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
        ):
            continue

    processes.sort(
        key=lambda x: x["cpu_percent"] or 0,
        reverse=True,
    )

    return processes[:10]


@server.tool()
def list_docker_containers() -> list:
    """List currently running Docker containers."""

    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--format",
                "{{.Names}}|{{.Image}}|{{.Status}}",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )

        if result.returncode != 0:
            return [
                {
                    "error": result.stderr.strip()
                    or "Docker command failed"
                }
            ]

        containers = []

        for line in result.stdout.strip().splitlines():

            if not line:
                continue

            parts = line.split("|", 2)

            containers.append(
                {
                    "name": parts[0],
                    "image": parts[1],
                    "status": parts[2],
                }
            )

        return containers

    except Exception as exc:
        return [{"error": str(exc)}]


if __name__ == "__main__":
    server.run()