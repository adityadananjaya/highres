# User Stories

## User Story 1

**ID:** 1

**As the analyst,** I want to know how a model performs on a folder of labeled images so that I can compare it to the performance of other models/other resolutions.

- **Functional Requirement:** The script needs to process the images and output a CSV file containing performance measures of each run, including such measures as accuracy, precision, recall, F1 score, and processing time. The script should take the folder as input (directory as a command line argument) and be able to process batch images of different resolutions through different models.
- **Non-Functional Requirement:** The script should be able to handle errors gracefully, so that when an unexpected error occurs, the results so far are saved (so that the time spent was not wasted).
- **Interface:** The interface of the script would simply be in the command line.

## User Story 2

**ID:** 2

**As the analyst,** I want to be able to combine multiple results CSV into one massive dataset so that I can take my teammates’ results and combine it with my own into one.

- **Functional Requirement:** The script should be able to take as input multiple directories for each of the CSV files and write a single CSV file with the concatenated data.
- **Non-Functional Requirement:** The merging process should be able to handle discrepancies like missing values or duplicate files and rows.
- **Interface:** The script can be interfaced through a command line argument.

## User Story 3

**ID:** 3

**As the analyst,** I want to interact with our produced results in a visual and interactive manner so I can more reliably and effectively make conclusions for our client based on those results.

- **Functional Requirement:** Users should have the option to select the particular resolutions or models they want to compare and how they want to visualize the results (e.g., box plots, histograms, etc.).
- **Non-Functional Requirement:** The app should be responsive, intuitive, and easy to use.
- **Interface:** This will be a user interface in the form of a data dashboard web app.

## User Story 4

**ID:** 4

**As the client,** I also want to interact with the results visually and interactively so I can convince myself of the team’s recommendations and conclusions.

- **Functional Requirement:** As above.
- **Non-Functional Requirement:** The important non-functional requirement is the ease of use and intuitiveness so that the client can navigate through the app without confusion.


### **More coming soon according to client feedback**.