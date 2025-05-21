# **Synchro Qt Made**

[Français](https://github.com/Patrick-81/Synchro-Qt-Made/blob/master/README.fr.md) | [English](https://github.com/Patrick-81/Synchro-Qt-Made/blob/master/README.md)

## **Directory Backup and Synchronization Application**

Synchro Qt Made is a robust and intuitive desktop application designed to automate the backup and synchronization of your important directories. It offers precise control over your data, with scheduling, filtering, and version management options.

## **Key Features**

* **Configuration Management:** Create, save, load, and delete custom synchronization profiles for different directories.  
* **Automated Synchronization:** Set an hourly frequency for your directories to be automatically synchronized in the background.  
* **Advanced Filtering:** Exclude specific files and directories from synchronization using configurable blacklists.  
* **Version Cache Management:** Keep a defined number of older versions of your modified files, preventing data loss while optimizing disk space.  
* **Real-time Monitoring:** Monitor the progress of ongoing synchronizations and their status via a clear graphical interface and a dynamic progress bar.  
* **Task Summary:** Get a detailed summary of past synchronization operations, including statistics (added, modified, deleted files/directories) and direct access to log files.  
* **Automatic Log Cleanup:** Application and task logs are automatically purged after one week to maintain disk space.  
* **Intuitive Interface:** A clear and easy-to-use PyQt5-based user interface, with visual customization options via a CSS style file.

## **Application Architecture**

The application is structured into three main components that communicate with each other:

* **Frontend (mainwindow.py):** The graphical user interface (GUI) built with PyQt5. It allows the user to configure tasks, start them, stop them, and view their status and logs.  
* **Backend (api.py):** A lightweight REST API server based on Flask. It acts as an intermediary, receiving requests from the frontend and managing the starting, stopping, and monitoring of synchronization processes.  
* **Synchronization Engine (sync\_engine.py):** A Python script executed as a separate process by the backend. It is the core of the synchronization logic, responsible for copying files, applying filters, managing frequency, and maintaining versions.

## **Installation**

Follow these steps to install and run the application.

### **Prerequisites**

* **Python 3.x** (recommended: Python 3.8 or newer)  
* **Git**

### **Installation Steps**

1. Clone the Git repository:  
   Open your terminal or command prompt and execute:  
   git clone https://github.com/your\_username/Synchro-Qt-Made.git \# Replace with your repository URL  
   cd Synchro-Qt-Made

2. Create requirements.txt files:  
   In the root of your project, create the following files:  
   * Synchro\_backend/requirements.txt with the content:  
     Flask  
     Flask-CORS

   * Synchro\_qt\_made/requirements.txt with the content:  
     PyQt5  
     requests

3. Create virtual environments (recommended) and install dependencies:  
   It is highly recommended to create separate virtual environments for the frontend and backend to manage dependencies.  
   \# For the backend  
   python3 \-m venv .venv\_backend  
   source .venv\_backend/bin/activate \# On Linux/macOS  
   \# .venv\_backend\\Scripts\\activate \# On Windows  
   pip install \-r Synchro\_backend/requirements.txt

   deactivate \# Deactivate backend environment

   \# For the frontend  
   python3 \-m venv .venv\_frontend  
   source .venv\_frontend/bin/activate \# On Linux/macOS  
   \# .venv\_frontend\\Scripts\\activate \# On Windows  
   pip install \-r Synchro\_qt\_made/requirements.txt

   deactivate \# Deactivate frontend environment

4. Verify file structure:  
   Ensure your project directory contains the Synchro\_backend and Synchro\_qt\_made folders, as well as the api\_client.py file at the root.

## **Initial Configuration**

Before launching the application, you need to configure some files.

### **1\. \~/.synchro/volume\_config.json**

This file manages the base paths for your destination volume and version cache settings.

* **Creation :** If the \~/.synchro/ directory and volume\_config.json file do not exist, they will be created automatically on the first launch of the frontend.  
* **Content (example) :**  
  {  
      "external\_volume\_base\_path": "/path/to/your/SynchroDestination",  
      "max\_cached\_versions": 2  
  }

  * Replace "/path/to/your/SynchroDestination" with the absolute path to your main destination directory. This is where synchronized directories will be created.  
  * "max\_cached\_versions": Set the number of older versions of a modified file to keep. 0 means no versions, 1 means the current version \+ the last modified version, etc.

### **2\. gui\_config.json**

This file, located in the Synchro\_qt\_made directory, allows customizing the user interface's appearance via CSS rules. You can edit it to change colors, fonts, sizes, etc.

## **Application Usage**

### **1\. Start the Backend**

The backend must be started first and remain active.

1. Open a new terminal.  
2. Activate the backend virtual environment:  
   cd Synchro-Qt-Made/Synchro\_backend  
   source ../.venv\_backend/bin/activate \# or .venv\_backend\\Scripts\\activate on Windows

3. Launch the backend:  
   python3 api.py

   You should see log messages indicating that the Flask server is running on http://127.0.0.1:7555.

### **2\. Start the Frontend**

Once the backend is running, you can start the user interface.

1. Open **another** new terminal.  
2. Activate the frontend virtual environment:  
   cd Synchro-Qt-Made/Synchro\_qt\_made  
   source ../.venv\_frontend/bin/activate \# or .venv\_frontend\\Scripts\\activate on Windows

3. Launch the frontend:  
   python3 mainwindow.py

   The application's graphical interface should appear.

### **3\. Configure and Start a Synchronization**

1. **Select Source :** In the "Source" field, click "Browse..." to choose the directory you want to synchronize.  
2. **Verify Destination :** The "Destination" field will automatically display the full path where your files will be backed up.  
3. **Set Frequency :** Use the "Frequency (hours)" field or the slider to specify the synchronization interval.  
4. **Configure Blacklists :** Add file and directory patterns to ignore in the "Blacklist Files" and "Blacklist Directories" fields (separated by semicolons).  
5. **Set Max Cached Versions :** Specify the number of older versions to keep.  
6. **Save Configuration :** Click "Save Configuration". The configuration name will be derived from your source directory name.  
7. **Start Synchronization :** Click the "Start" button. The button will turn red, and the progress bar will activate, displaying the task's status.

### **4\. Manage Tasks and Logs**

* **Stop :** Click "Stop" to stop an ongoing synchronization.  
* **Load Configuration :** To resume a previously saved configuration. The interface will automatically check if the corresponding synchronization is already running on the backend and update its status.  
* **Summary :** Displays a summary of synchronization tasks (active and completed) in the log area, with detailed statistics and clickable links to each task's specific logs.  
* **Clear Log / Copy Log :** Allow managing the content of the interface's log area.

## **Troubleshooting**

* **"Backend unreachable" :** Ensure the api.py script is running in its own terminal and that there are no errors on backend startup. Verify that port 7555 is free.  
* **Synchronization does not start :** Check the frontend logs (\~/.synchro/logs/app.log) and backend logs (\~/.synchro/logs/backend\_app.log) for error messages. Ensure that source and destination paths are valid and that you have necessary access permissions.  
* **Progress bar not updating / "Start" button still green after loading :** This means the synchronization for the selected configuration is not active on the backend. Start it manually or check the logs to understand why it didn't start or was stopped.  
* **Version cache issues :** Check the max\_cached\_versions value in volume\_config.json and in the interface. The cache cleanup logic is implemented in sync\_engine.py ; consult the specific task logs for detailed information.

## **Contribution**

If you wish to contribute to this project, feel free to fork the repository, make your changes, and submit pull requests.

## **License**

\[To be added: Specify your project's license here (e.g., MIT, GPL, Apache 2.0)\]
