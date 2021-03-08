import os.path
import setuptools

repository_dir = os.path.dirname(__file__)

with open(os.path.join(repository_dir, "requirements.txt")) as fh:
    requirements = [line for line in fh.readlines() if not line.startswith("--")]

setuptools.setup(
    name="torrnodes-scheduler",
    version=1.0,
    author="Adel Bibi",
    python_requires=">=3.7",
    description="GPU scheduler for torrnodes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "torrnodes_gpu_crawler = torrnodes_scheduler.gpu_crawler:main",
            "torrnodes_free_gpus = torrnodes_scheduler.scheduler_monitor:avail_gpus",
            "torrnodes_run_commands = torrnodes_scheduler.scheduler_monitor:run_commands"
        ]
    },
    include_package_data=True,
)
