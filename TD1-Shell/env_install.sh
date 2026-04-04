#!/bin/bash

print_message() {
    printf "\n========================================\n"
    printf "%s\n" "$1"
    printf "========================================\n\n"
}

# Detecting OS
OS="Linux"
PKG_MANAGER="apt-get"
print_message "Target OS: Debian/Linux"

# check python
check_python() {
    print_message "Checking for Python3..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version)
        print_message "Python3 is already installed: $PYTHON_VERSION"
    else
        print_message "Python3 not found. Installing..."
        sudo apt-get update
        sudo apt-get install -y python3
        print_message "Python3 installation complete"
    fi
}


# Verify pip is available
check_pip() {
    print_message "Checking for pip..."
    
    if command -v pip3 &> /dev/null; then
        PIP_VERSION=$(pip3 --version)
        print_message "pip is available: $PIP_VERSION"
    else
        print_message "pip not found. Installing pip3..."
        sudo apt-get update
        sudo apt-get install -y python3-pip
        print_message "pip3 installation complete"
    fi
}


# Install Jupyter Notebook
install_jupyter() {
    print_message "Installing Jupyter Notebook..."
    
    pip3 install jupyter
    
    print_message "Jupyter Notebook installation complete"
}


print_message "Starting Development Environment Setup" 
check_python
check_pip
install_jupyter
print_message "Setup Complete! Your development environment is ready."
