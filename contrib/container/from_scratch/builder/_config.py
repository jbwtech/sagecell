
# Container names
IMAGE_BASE = "base"      # OS and packages
IMAGE_SAGE = "sage"      # Sage without extra packages
IMAGE_PRECELL = "precell"    # Everything but SageCell and system configuration
IMAGE_SAGECELL = "sagecell"      # Sage and SageCell
IMAGE_BACKUP = "sagecell-backup"     # Saved master for restoration if necessary
IMAGE_TESTER = "sctest"  # Accessible via special port, for testing
IMAGE_PREFIX = "sc-"     # Prefix for main compute nodes


# Theses are the lists of packages to install
filelist = [
    "lists/base/prerequisites.txt",
    "lists/base/recommended.txt",
    "lists/base/optional.txt",
    "lists/base/R.txt",
]

