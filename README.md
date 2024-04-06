# xtream AI Challenge

## Ready Player 1? 🚀

Hey there! If you're reading this, you've already aced our first screening. Awesome job! 👏👏👏

Welcome to the next level of your journey towards the [xtream](https://xtreamers.io) AI squad. Here's your cool new assignment.

Take your time – you've got **10 days** to show us your magic, starting from when you get this. No rush, work at your pace. If you need more time, just let us know. We're here to help you succeed. 🤝

### What You Need to Do

Think of this as a real-world project. Fork this repo and treat it as if you're working on something big! When the deadline hits, we'll be excited to check out your work. No need to tell us you're done – we'll know. 😎

🚨 **Heads Up**: You might think the tasks are a bit open-ended or the instructions aren't super detailed. That’s intentional! We want to see how you creatively make the most out of the data and craft your own effective solutions.

🚨 **Remember**: At the end of this doc, there's a "How to run" section left blank just for you. Please fill it in with instructions on how to run your code.

### How We'll Evaluate Your Work

We'll be looking at a bunch of things to see how awesome your work is, like:

* Your approach and method
* Your understanding of the data
* The clarity and completeness of your findings
* How you use your tools (like git and Python packages)
* The neatness of your code
* The readability and maintainability of your code
* The clarity of your documentation

🚨 **Keep This in Mind**: This isn't about building the fanciest model: we're more interested in your process and thinking.

---

### Diamonds

**Problem type**: Regression

**Dataset description**: [Diamonds Readme](./datasets/diamonds/README.md)

Meet Don Francesco, the mystery-shrouded, fabulously wealthy owner of a jewelry empire. 

He's got an impressive collection of 5000 diamonds and a temperament to match - so let's keep him smiling, shall we? 
In our dataset, you'll find all the glittery details of these gems, from size to sparkle, along with their values 
appraised by an expert. You can assume that the expert's valuations are in line with the real market value of the stones.

#### Challenge 1

Plot twist! The expert who priced these gems has now vanished. 
Francesco needs you to be the new diamond evaluator. 
He's looking for a **model that predicts a gem's worth based on its characteristics**. 
And, because Francesco's clientele is as demanding as he is, he wants the why behind every price tag. 

Create a Jupyter notebook where you develop and evaluate your model.

#### Challenge 2

Good news! Francesco is impressed with the performance of your model. 
Now, he's ready to hire a new expert and expand his diamond database. 

**Develop an automated pipeline** that trains your model with fresh data, 
keeping it as sharp as the diamonds it assesses.

#### Challenge 3

Finally, Francesco wants to bring your brilliance to his business's fingertips. 

**Build a REST API** to integrate your model into a web app, 
making it a cinch for his team to use. 
Keep it developer-friendly – after all, not everyone speaks 'data scientist'!

#### Challenge 4

Your model is doing great, and Francesco wants to make even more money.

The next step is exposing the model to other businesses, but this calls for an upgrade in the training and serving infrastructure.
Using your favorite cloud provider, either AWS, GCP, or Azure, design cloud-based training and serving pipelines.
You should not implement the solution, but you should provide a **detailed explanation** of the architecture and the services you would use, motivating your choices.

So, ready to add some sparkle to this challenge? Let's make these diamonds shine! 🌟💎✨

---

## How to run

The first step that is valid for every challenge is setting up a Python Environment: this guide will walk you through the process for setting up a new PC without Python.

#### Step 1: Download and Install Python

- Open your web browser and navigate to the official Python website: python.org.  
- Click on the "Downloads" tab located on the top navigation bar and choose.  
- Choose the **python version 3.10** for your operating system (Windows, macOS, or Linux) and click on the download link.  
- Once the download is complete, run the installer and follow the installation instructions provided.  

#### Step 2: Verify Python Installation

- After the installation is complete, open your terminal, type `python --version` and press Enter. This command should display the installed Python version.  
- Check that the version is `3.10`

### Challenge 1

#### Step 1: Install Jupyter Notebook

- Open the command prompt or terminal, type `pip install notebook` and press Enter.  
- Wait for the installation to complete. Once finished, Jupyter Notebook is installed on your system.  

#### Step 2: Launch the Notebook

- Navigate to *xtream-ai-assignment-engineer/src/challenge_one* using the command prompt or terminal.  
- Type `jupyter notebook diamonds_notebook.ipynb` and press Enter.  
- This will open a new tab in your web browser displaying the Jupyter Notebook dashboard.

#### Step 3: Work with the Notebook

- From here you can work with the notebook, running individual cells or going to the top menu to Run>Run All Cells to run the whole notebook.

### Challenge 2

#### Step 1: Setting Up the Environment

- Ensure that you have the necessary dependencies installed.  
- Open the terminal in *xtream-ai-assignment-engineer*, type `pip install -r requirements.txt` and press Enter.  

#### Step 2: Execute the code

- Navigate to *xtream-ai-assignment-engineer/src/challenge_two* using the command prompt or terminal.  
- Type `python automated_diamond_model.py` and press Enter.
- The model will be trailed automatically with the baseline data, and information on the time taken and its evaluation will be provided, again from a provided test set.  

#### Step 3: Train the model with new data

- After the model is trained there will be the question **Do you want to keep process alive to watch the folder for new data?**.  
  - If answered with **y** the process will stay waiting for new data.  
- Data can be uploaded to the xtream-ai-assignment-engineer\datasets folder.  
- The file must be in `.CSV` format and must contain the following columns: *carat, cut, color, clarity, depth, table, price, x, y and z*.  
- As soon as the new file is detected you will be asked **Do you want to train the model with this file?**.  
  - If answered with **y** the data will be preprocessed and used to strengthen the model.  
- The new performance evaluations will then be provided.  

> **_NOTE:_**  In this case there is already a src/challenge_two/new_diamonds_test.csv file only for testing purposes only.  
> The file consists of the first 20 rows of the original diamonds.csv file, so performance will probably decrease if it will be used.
### Challenge 3

#### Step 1: Setting Up the Environment

- Ensure that you have the necessary dependencies installed.  
- Open the terminal in *xtream-ai-assignment-engineer*, type `pip install -r requirements.txt` and press Enter.  

#### Step 2: Open the web app

- Navigate to *xtream-ai-assignment-engineer* using the command prompt or terminal.  
- Type `streamlit run src/challenge_three/webapp.py` and press Enter.
- A page will be opened in the default browser. If not, simply click on the Local URL link that will appear in the terminal.
- When the web app is opened, the model will be towed automatically.  

#### Webapp structure and how to use it
- There are four different section in the webapp: *Model Training*, *Price Prediction*, *Price History* and *Train with new data*.  
  - **Model Training**: the performance are noted and with the button is possible to retrain the model at any time.  
  - **Price Prediction**: inserting a diamond dimensions and features is possible to predict its price.  
  - **Price History**: here are stored all the previous price prediction. It is possible to clean the history.  
  - **Train with new data**: drag-and-drop a CSV file and it will be uploaded. There will be a checkbox and a button
    - The checkbox will show or hide a table containing the data provided.
    - The button will reinforce the model with those data. It is possible to use the `new_diamonds_test.csv` of the second challenge.