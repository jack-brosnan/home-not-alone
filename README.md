# ![Project Logo](staticimagestplogo.png)

# Welcome to Home Not Alone!

## The Secret Santa Planning App
### Home Not Alone is dedicated to making planning your next Secret Santa super simple, while keeping everyone's secret gifts a Santa-sized surprise!

The responsive website allows registered users to create participant lists for gift giving activities, allowing easy inviting and assignment distribution, along with setting a recommended budget for all gifts involved. Users who are not registered are recommended to check out the website's About page, and are free to sign up for their own account. 

# [Link to Live Site](#)  

This project is created as a final hackathon project for Code Institute's 16 week fullstack developer bootcamp.  

Built by Team "Santa's Little Nerds": Jack, Bryan, Oleksii and Emma.

---

# Table of Contents  

 1. [UX](#ux)
 2. [Agile Development](#agile-development)
 3. [Features Implemented](#features-implemented)  
 4. [Features Left to Implement](#features-left-to-implement)  
 5. [Technology Used](#technology-used) 
 6. [Testing](#testing-and-validation)  
 7. [Bugs](#known-bugs)  
 8. [Deployment](#deployment)
 9. [Resources](#resources)  
 10. [Credits and Acknowledgements](#credits-and-acknowledgements)

---

# UX

## Database Planning

Describe your database planning process and include diagrams if available.
![Database Entity Relationship Diagram](pathtoyourdiagram.png)

## UX Design

### Overview
Provide a brief overview of the UX design and user experience goals.

### Site User
Describe the primary users of your site.

### Goal
Explain the main goal of your site.

## Wireframes

Include your wireframes here.
![Wireframe Example](pathtoyourwireframe.png)

##### [ Back to Top ](#table-of-contents)

# Agile Development

When collaborating on ideas for our group project, we created a dedicated Miro board. We ideated on our plans, broke it down into pieces to examine the purpose and target audience, and determined what key elements were needed for both the UX design and the Entity Relationship Diagram for Django.   
- [Home-not-Alone Planning Board](https://miro.com/app/board/uXjVL2ywJpk=/?share_link_id=472010981286)

We also set up a kanban board for tracking our project's user stories on GitHub's Projects site. Our project board can be found here: [Home-not-Alone Project Board](https://github.com/users/jack-brosnan/projects/9)


### User Stories Overview

1. _User Story 1: Create and Manage Events_
- As a organiser I can create a new Secret Santa event so that I can easily host a gifting exchange for my group.

2. _User Story 2: Account Registration_
- As an organiser, I can easily find the sign up page and create an account on the website that will let me host a gifting exchange for my group.
- As a participant, I can easily accept the invite link and create an account to join my secret santa's group.

3. _User Story 3: Event Details_
- As an organiser, I can create a new group with appropriate settings that will allow me to invite the correct participants.
- As a participant, I can see what gift giving group I am a member of and the relevant requirements for the group.

4. _User Story 4: Participant Profile_
- As an organiser, I can clearly see the names of all participants and who they have been assigned as their gift recipient.
- As a participant, I can clearly see the name of my drawn gift recipient.
- As a participant, I can add, modify and delete a wish list that will be shown to my gift giver.

5. _User Story 5: Secret Santa site theming_
- As a site administrator, I want to have strong colour palette and appearance choices for my website's appearance - so that it fits both the holiday season and the site's theme.

6. _User Story 6: Landing Page_
- As a site user, I want a landing page that introduces me to the secret santa website.

7. _User Story 7: About Page_
- As a site user, I want a landing page that introduces me to the secret santa website.

##### [ Back to Top ](#table-of-contents)

# Features Implemented

List and describe the features implemented in your project.

## Home Page
- Feature 1
- Feature 2

## About Page
- Feature 1
- Feature 2

## Profile Page
- Feature 1
- Feature 2

## Login Page
- Feature 1
- Feature 2

## Registration Page
- Feature 1
- Feature 2

## Logout Page
- Feature 1
- Feature 2

### Responsive Design
- Feature 1
- Feature 2

## Additional Security Features
- Feature 1
- Feature 2

##### [ Back to Top ](#table-of-contents)

# Future Features

List and describe the features you plan to implement in the future.

##### [ Back to Top ](#table-of-contents)

# Technology Stack

List the technologies used in your project.

- Technology 1
- Technology 2
- Technology 3

##### [ Back to Top ](#table-of-contents)

# Testing and Validation

Describe your testing and validation process.

### HOME PAGE

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

### ABOUT PAGE

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

### PROFILE PAGE

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

### LOGIN PAGE

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

### REGISTRATION PAGE

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

### LOGOUT PAGE

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

### SECURITY

 Test                                      Result 
-------------------------------------------------
 Test description                         Pass   

##### [ Back to Top ](#table-of-contents)

# Known Bugs

List any known bugs here.

##### [ Back to Top ](#table-of-contents)

# Deployment 

## Deployment Guide

### Deployment Steps

#### Creating the Heroku App

- Begin by signing up OR logging in to [Heroku](https://www.heroku.com/).
- In the Heroku Dashboard, click on 'New'.
- Select 'Create New App'.
- Next, choose a unique name for your project.
- Select the appropriate region. For example: "EU region".
- Click "Create App" to proceed.
- In the "Deploy" tab, choose GitHub as the deployment method.
- Connect your GitHub account and find/connect your GitHub repository to complete the link.

#### Setting Up Environment Variables

- Create `env.py` in the top level of the Django app.
- Import `os` in `env.py`.
- Set up necessary environment variables in `env.py`. This includes the secret key and database URL.
- Update `settings.py` to use environment variables for secret key and database correctly.
- Configure environment variables in the Heroku "Settings" tab, under "Config Vars".
- Migrate the models to the new database connection in the terminal.
- Configure the static files and templates directories in your `settings.py`.
- Add Heroku to the `ALLOWED_HOSTS` list.

#### Creating Procfile and Pushing Changes

- Create a `Procfile` in the top level directory of your repository.
- Next, add the command to run the project in the `Procfile`.
- Add, commit, and push these changes to GitHub.

#### Heroku Deployment

- In Heroku, navigate to the Deployment tab.
- Click to deploy the branch manually.
- You should then monitor the build logs for any errors that may occur.
- Upon successful deployment, Heroku will display a link to the live site for your app.
   - Make sure to resolve any deployment errors by adjusting the code as necessary!

### Forking the Repository

Forking the GitHub Repository will allow you to create your very own copy of the original repository without affecting the original. Follow these steps to do so:

- Log in to GitHub OR create a GitHub account.
- Visit the [repository link](https://github.com/jack-brosnan/home-not-alone).
- Click on "Fork" at the top of the repository.

### Creating a Clone of the Repository

Creating a clone of a repository enables you to make a local copy of said repository. Follow these steps to proceed:

- Navigate to the [Home not Alone repository](https://github.com/jack-brosnan/home-not-alone).
- Click on the <>Code button.
- Select the "HTTPS" option under the "Local" tab.
- Copy the URL.
- Open your IDE terminal and change the directory to your desired location.
- Use `git clone` followed by the copied repository URL.
- You now have your own copy of Home not Alone!

##### [ Back to Top ](#table-of-contents)

# Resources

- [Resource 1](#)
- [Resource 2](#)

##### [ Back to Top ](#table-of-contents)

# Credits and Acknowledgements

## Images

- [Fancaps.net](https://www.fancaps.net) - Home Alone screenshots used for placeholder and site images.
- Source 2

## Code

- [Django Invitations](https://django-invitations.readthedocs.io/en/latest/)
- [StackOverflow](https://stackoverflow.com/questions/67361758/how-do-i-effectively-add-sound-to-a-button-in-html-or-css) - Adding sound effects for button press.

## Credit

##### [ Back to Top ](#table-of-contents)