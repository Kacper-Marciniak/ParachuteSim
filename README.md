# PWrInSpace - parachute simulator

Simple software to determine parachute parameters for the sounding rocket design process.
This software is developed as part of the PoliWRocket project of the [PWrInSpace](https://pwrinspace.pwr.edu.pl/) student association.

## Prerequisites

### Anaconda Installation

Before you begin, make sure you have Anaconda installed. You can download it from the [official Anaconda website](https://www.anaconda.com/products/distribution).

1. Download the Anaconda version suitable for your operating system.
2. Follow the Anaconda installer instructions.

### Creating a New Environment

After installing Anaconda, create a new environment using the terminal or Anaconda Prompt:

```bash
conda create --name environment_name python=3.11
```

### Activate the environment:

```bash
activate environment_name
```

### Installing pip

Ensure that the pip tool is installed in your environment:

```bash
conda install pip
```

### Installing Packages from requirements.txt

Navigate to the project location using the cd command and install the packages listed in the [requirements.txt](requirements.txt) file:

```bash
cd /path/to/project
pip install -r requirements.txt
```

## Running a ParaSim from command line

1. Open Anaconda Prompt.
2. Activate the environment:

```bash
activate environment_name
```

3. Navigate to the directory where the Python script is located using the cd command:

```bash
cd /path/to/project
```

4. Run the script using the following command:

```bash
python app.py
```

Application should be available at the: [http://127.0.0.1:8080/](http://127.0.0.1:8080/).