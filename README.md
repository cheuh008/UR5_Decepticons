# Decepticons Project: GNU Edition

Team Memebrs:

Megan **Megatron** O'neil
Harry **Shockwave** Cheung
Justin **Starscream** 
Marion **Skywarp** Reidgway


---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
   - [Git Basics](#git-basics)
   - [Python with Conda](#python-with-conda)
3. [License](#license)

---

## Project Overview

---

## Getting Started

Git makes collaborating in a team easier and more streamlined by enabling branches which isolate individual changes and makes it more developmentally stable to merge with the main branch with pull requests once the code is tested and stable

### Git Basics

To contribute to the Decepticons Project, you'll need to use Git. Here are some basic commands to get you started:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/cheuh008/UR5_Decepticons
    ```

2. **Use a Branch to keep your work safe**
   ```bash
   git checkout Megatron

   git checkout Soundwave

   git checkout Starscream

   git checkout Skywarp
   ```
   or make your own branch:
   ```bash
      git checkout -b [branch-name]
   ```


3. **Make Changes and Commit:**
   ```bash
   git add . 
   git commit -m "[message]"
    ```
   A descriptive message of the changes you've made is encouraged
   . adds all files but files can be indicidually specified
   
4. Push Your Changes:
   ```bash
   git push origin [your-branch-name]
    ```
---

Python with Conda
- Following on from Joe's project, we are using conda again to manage Python packages (modules you import) More info [here](https://docs.anaconda.com/).
- Anaconda (conda) is an open-source environment management system (that makes sure that Python is uniquely the same across projects and that there are no incompatibilities.)
- VS Code automatically prompts you to use a virtual environment when working with Python files. If setup, this "venv" can be [selected](https://code.visualstudio.com/docs/python/environments):

1. Create a Conda Environment:
```bash
conda create -n [env-name] (python version can be specified as python=3.X)
conda activate [env-name]
```
2. Install Dependencies:
```bash
pip install -r requirements.txt
```

---
License
This project is licensed under the GNU General Public License (GPL). See the LICENSE file for details.
---

***Contact and support***
Harry **Shockwave** has nothing better to do andis always at your service at h.cheung10@liv.ac.uk

