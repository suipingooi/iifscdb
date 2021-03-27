## Code Institute Milestone Project 3 - Python and Data Centric Development

### IIFSC Database

This project aims to ....

<hr>

#### Island Ice Figure Skating Club (IIFSC) - Background
![Island Ice Figure Skating Club](static/assets/images/iifsc.webp) <br>
Island Ice Figure Skating Club is a social ice skating club formed to provide support to our figure skater members and families. IIFSC focuses on building rapport, camaraderie and harmony within the ice skating community by initiating and organizing a variety of activities that promotes such values through fun/play. IIFSC believes that it takes a village to raise a child and aims to create a strong tribe to support each and every individual skater (and family) to reach their individual skating goals. IIFSC logo represents the blades and scratch lines made when a figure skater draws/cuts an image on ice. Both blades were chosen in pink and blue to signify gender neutrality whislt one being larger than the other as a representation of a parent/educator/coach and child/student.

IIFSC is also the home club for a number of Singapore's National Squad team members.

### UX - User Experience

Wireframe of the build design includes:

![Wireframe](#)

<hr>

![Color Chart](static/assets/images/readme/iifsc_colorchart.png)<br>

<img src="static/assets/images/readme/tn_colors/79f2e6.png" alt="#79F2E6" width="30px"> BLUE denotes stability, balance, and harmony <br>
<img src="static/assets/images/readme/tn_colors/ff55aa.png" alt="#FF55AA" width="30px"> RED symbolizes power and energy. PINK symbolizes unconditional love and support <br>
<img src="static/assets/images/readme/tn_colors/faeaaa.png" alt="#FAEAAA" width="30px"> YELLOW is associated with spontainety and flexibility <br>
<img src="static/assets/images/readme/tn_colors/black.png" alt="black" width="30px"> BLACK symbolizes elegance and sophistication <br>

<hr>

![Font Gylps](#)<br>

<hr>

A demo of the site can be found here [#](#)

![Interactive Web Design](#)


## Built With 
### Technologies
1. HTML 5.0 + CSS as core language for frontend UI.
2. Bootstrap 5.0 - CSS & JS [https://getbootstrap.com/](https://getbootstrap.com/)
3. Python 3 + Flask [https://www.python.org/](https://www.python.org/) and [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/) as core language for backend processing.
4. MongoDB Atlas [https://www.mongodb.com/cloud/atlas/](https://www.mongodb.com/cloud/atlas) as database handler.
5. Cloudinary [https://cloudinary.com/](https://cloudinary.com/) for image hosting of uploaded image files.
6. Heroku [https://www.heroku.com/](https://cloudinary.com/) as deployment host.

### Styling
1. Google Fonts [https://fonts.google.com/](https://fonts.google.com/) for font-family pairings.
2. Fontawesome [https://fontawesome.com/](https://fontawesome.com/) for icons.
3. Gimp 2.10 [https://www.gimp.org/](https://www.gimp.org/) for image manipulation.
4. Adobe Color [https://color.adobe.com/](https://color.adobe.com/) to extract IIFSC base color chart.


### Testing
[W3C Validator](https://validator.w3.org/) for html validation. All errors dealt with save for Jinja templating errors/ warnings.

[Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/) for css validation. no errors found.

<hr>

| Action (development testing)             | Results                       | Status      |
| -----------------------------------------|:-----------------------------:|-------------|
| Form submissions - empty form            | Alert prompts fixed           | Completed   |
| Form submissions - invalid data          | Alert prompts fixed           | Completed   |
| Form validation algorithm                | Errors fixed                  | Completed   |                         
| Algorithm testing (datetime, calc)       | Errors fixed                  | Completed   |
| Mongodb CRUD tests                       | Errors fixed                  | Completed   |         
| All buttons and links                    | Corrected paths               | Completed   |
| Responsive pages                         | non-responsive elements fixed | Completed   |

| <h3>**User Features Tests during development**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Test 1: Hyperlinks of navigation tabs / hamburger dropdowns with multiple screen size.**                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Expected:** 1. Navbar brings me to different specified pages with external links opening in a new tab. 2. Navbar turns to hamburger dropdown when screensize drops. <br> **Test:** Clicking on all different links to reload multiple times. <br/>**Result:** Multiple issues with background image for different screen size noted; navigation controls works as expected.<br/>                                                                                                                                                           |
| **Test 2: Coaches & Students pages.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **Expected:** On load, pages should list individual profile cards with profile image and basic data of coaches/students in the database complete with edit+delete icons; newest entry first.<br/>**Test:** Click on buttons located in index page or from navbar; adding new entry into database with form. <br/>**Result:** Pages loads & reloads as expected.<br/>                                                                                                                                                                         |
| **Test 3: Requests page.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Expected:** On load, a list of lesson request will appear in a table format with detail+delete icons. <br> **Test:** Click on buttons located in index page or from navbar; adding new entry into database with form. <br>**Results:** Page loads as expected; however, table does not support screen rezising for responsive UI/UX noted. Fixed with mediascreen breakpoints                                                                                                                                                              |
| **Test 4: Rinks page.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Expected:** On load, rinks detail card will appear with visit website button.<br> **Test:** Click on link from navbar. <br>**Results:** Page loads as expected.                                                                                                                                                                                                                                                                                                                                                                            |
| **Test 5: MongoDB CRUD tests for Coaches + Lesson Requests(schedule) collections.**                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Expected:** Data entry/updates of new coaches and lesson requests via forms uploads into MongoDB and translated into a card entry in coaches page/lesson request submission in requests page with redirects. On cick of delete icon, users will be asked to confirm delete and entry removed from mongoDB database collection. <br> **Test:** Click btn(Add New) coach + btn(Request Lesson) to add new entries via forms, click on edit/delete icons to update or delete** . <br>**Results:** Multiple errors with datatypes noted. Fixed |
| **Test 6: MongoDB CRUD tests for Students (+ embed data of historical competition results) collections.**                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Expected:** Data entry/updates of new students and competition data via forms uploads into MongoDB and translated into a card entry in students page/competition data in skater's individual profile page with redirects. On cick of delete icon, users will be asked to confirm delete and entry removed from mongoDB database collection. <br> **Test:** btn(Add New) student + btn(More Info) to add new entries via forms, click on edit/delete icons to update or delete** . <br>**Results:** Issues with datetime inputs noted. Fixed|                                                                                           
| **Test 7: Database search on all pages.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Expected:** Listing of only data matching entry of searched criteria. <br> **Tests:** input criteria and click search. <br>**Results:** As expected.                                                                                                                                                                                                                                                                                                                                                                                       |                                                                                                                                                                                                                                                                                        
| **Test 8: Validation of forms**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Expected:** Form will display error message if unable to process forms. <br> **Tests:** submission of blank form or invalid data patterns; submission uploads of unsupported filetype.** <br>**Results:** Multiple failures noted with datetime and file upload inputs. Fixed                                                                                                                                                                                                                                                              |                                                                                                                                                                                                                                                                                        
| **Test 9: Algorithm validation.**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Expected:** Datetime manipulation / age calcalations to be on point. Lesson requests must have 48hours lead time. DOB entry will not accept 3 < students > 80 <br> **Test:** submission of multiple combination of dates for students date of birth for age calculations and date and time for lesson requests. <br>**Results:** Error in original mathematical expressions. Fixed                                                                                                                                                         |                                                                                                                                                                                                                                                                                        
<hr>

| Action (deployed testing)                | Results             | Status   |
| -----------------------------------------|:-------------------:|----------|
| Loading deployed page on iOS mobile      | Bkg image issues    |          |
| Loading deployed page on android mobile  |                     |          |
| Loading deployed page on Firefox         |                     |          |
| Loading deployed page on Chrome          |                     |          |
| Loading deployed page on Safari          |                     |          |
| Responsive testing on Firefox            |                     |          |
| Responsive testing on Chrome             |                     |          |
| Logo hyperlink                           |                     |          |
| IG icon hyperlink                        |                     |          |
| Profile card hyperlink                   |                     |          |
| Tab navigations                          |                     |          |
| Form submissions - invalid response      |                     |          |
| Form submissions - empty form            |                     |          |
| Form submissions - float & integers      |                     |          |
| Form submissions - submit                |                     |          |
| Form validations                         |                     |          |
| Hyperlinks in readme.md                  |                     |          |

<hr>

## Features
### Existing Features
1. 

### Features left to Implement
1. 

## Deployment

## Credits

#### Content
1. https://docs.python.org/3/library/datetime.html#timedelta-objects
2. https://www.guru99.com/date-time-and-datetime-classes-in-python.html
3. https://flask-pymongo.readthedocs.io/en/latest/
4. https://jinja.palletsprojects.com/en/2.11.x/
5. https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
6. https://www.seekpng.com/ima/u2w7i1y3y3i1r5i1/
7. https://pixabay.com/



#### Media
1.

## Acknowledgments
1. 