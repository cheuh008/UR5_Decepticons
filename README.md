# Decepticons Project: Transforming Chemistry with AI-Drive Robotics

### **Team Lead:** Megan **_Megatron_** O'Neill
####  Full-Stack Developer and Project Manager
---
## Team Memebrs:
#### Cheif Data Scientist and Systems Engineer  
 - Harry **_Soundwave_** Cheung
#### Cheif Frontend Developer and Creatives Director.
 - Justin **_Starscream_**
#### Cheif Automation Engineer and Data Collector 
- Marion * **_Skywarp_** Ridgeway

---
## Project Overview

UR5 Robot... 
---
## Table of Contents
1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
   - [Git Basics](#git-basics)
   - [Python with Conda](#python-with-conda)
3. [License](#license)

---
## Getting Started

Git makes collaborating in a team easier and more streamlined by enabling branches which isolate individual changes and makes it more developmentally stable to merge with the main branch with pull requests once the code is tested and stable

---
### Git Basics
To contribute to the Decepticons Project, you'll need to use Git. Here are some basic commands to get you started:
1. **Clone the Repository**:

 - Open a terminal or vs code in your working directory and run the following code to clone the folder
   
   ```bash
   git clone https://github.com/cheuh008/UR5_Decepticons
   ```
   
2. **Checkout or Create a Branch**

- This helps isolate your work and changes made to your files that you want to work on
- So that everyone can work on their own stuff whenever they want to
  
   ```bash
   git checkout Megatron
   ```
   ```bash
   git checkout Soundwave
   ```
   ```bash
   git checkout Starscream
   ```
   ```bash
   git checkout Skywarp
   ```
3. **Pull the latest update from main**

 - to make sure that your brnach is up to date with any changes to main before and after you work
   
   ```bash
   git pull origin main
   ```
   
4. **Make Changes and Commit:**

 - Now any work that you've done you can either add them all or just the files you worked on

   ```bash
   git add . 
   git commit -m "[message]"
   ```
   A descriptive message of the changes you've made is encouraged
   . adds all files, but files can be individually specified as just filename or/directory/filename.file
   keep in mind that more things tyou add, the more likely there will be "conflict" with other updates
   
5. Push Your Changes to your branch:
   ```bash
   git push origin [your-branch-name]
   ```
6. **Pull again! --rebase**
- After committing and saving your work, and *definitely* before *Merging*
- Pull from main again to make sure that all the changes and updates are synced up and any conflicts are resolved,
   - ie either merging with the updated content or debugging to make sure updates are compatible
    ```bash
   git rebase main
   ```
*  - --rebase is used to avoid unnecessary merge commits and from the main brnach and reapplying your commits over the top
   - conflicts will arise from updated files and vs code is usually pretty good about merging conflicts but its a good idea to double check.
   - once resolved you can stage the resolved changes via
   ```bash
   git add . 
   ```
   and then
   ```bash
   git rebase --continue
   ``` 
7.  **Finally, Once *tested*, it can merge with the main Branch**
    ```bash
    git merge main
    ```

 for a list of all git commands do git help or: 
 ```bash
  git help -a
 ```
---

Python with Conda
- Following on from Joe's project, we are using conda again to manage Python packages (modules you import). More info [here](https://docs.anaconda.com/).
- Anaconda (conda) is an open-source environment management system (that ensures that Python is uniquely the same across projects and has no incompatibilities.)
- VS Code automatically prompts you to use a virtual environment for Python files. If set, this "venv" can be [selected](https://code.visualstudio.com/docs/python/environments):

1. Create a Conda Environment:
```bash
conda create -n [env-name] (python version can be specified as python=3.X)
conda activate [env-name]
```
2. Install Dependencies:
```bash
pip install -r requirements.txt
```

## Further Reading into Vision Language Models

- [Vision Language Models Explaine}([https://huggingface.co/blog/vlms)


---
License
This project is licensed under the GNU General Public License (GPL). See the LICENSE file for details.
---

***Contact and support***
Harry **Shockwave** has nothing better to do and is always at your service at h.cheung10@liv.ac.uk.

For complaint please seek Megan.oneil@totoallyRealemailaddress.biz

