# default.py
#
# This file maps ids to a string of classes.  Templates that use class_tags and insert_classes refer to this file.
# Note that some of the "ids" are more like class names.  These rules act like "macro expansions" in the templates.

# If True, the classes will be inserted.  Otherwise, the tags will be empty strings.
RETURN_CLASSES = True

CSS_IMPORTS = """
<link rel="stylesheet" href="{0}css/{1}/screen.css" media="screen">
<link rel="stylesheet" href="{0}css/{1}/print.css" media="print">
<link rel="stylesheet" href="{0}css/{1}/jquery-ui.css">
<!--[if lt IE 8]><link rel="stylesheet" href="{0}css/{1}/ie.css" 
type="text/css" media="screen, projection"><![endif]-->

<link rel="stylesheet" href="{0}frontendadmin/css/frontendadmin.css" />
<link rel="stylesheet" href="{0}uni_form/uni-form.css" />
"""

JS_IMPORTS = """
<script src="{0}js/jquery-1.4.2.min.js" type="text/javascript"></script>
<script src="{0}js/jquery-ui-1.8.1.custom.min.js" type="text/javascript"></script>
<script src="{0}js/jquery.countdown.pack.js" type="text/javascript"></script>
"""

CSS_IDS = {
  "header": "span-24 last",
  
  "home-energy": "span-11",
  "home-activities": "span-11 prepend-1 last",
  "home-news": "span-6 prepend-2",
  "home-prizes": "span-6 prepend-7 last",
  "home-learn": "span-6 prepend-5",
  "home-profile": "span-6 prepend-1 last",
  
  "news-events+popular+activities": "span-8",
  "news-wall": "span-15 prepend-1 last",
  
  "profile-form": "span-8",
  "profile-badges": "span-8",
  "profile-history": "span-8 last",
  
  "landing-logo": "span-3",
  "landing-title": "span-21 last",
  "landing-intro": "span-12",
  "landing-poster": "span-12 last",
  "landing-page": "span-24 last",
  "landing-poster": "",
  "landing-sponsors": "span-24 last",
  
  "energy-power+scoreboard": "span-6",
  "energy-status": "span-18 last",
  
  "activity-events+scoreboard": "span-9",
  "activity-categories": "span-15 last",
  "activity-category": "ui-accordion-content ui-widget-content ui-corner-all ui-accordion-content-active",
  
  "prizes-list": "span-11",
  "prizes-raffle": "span-13 last",
  "prizes-info": "span-10 last",
  
  "help-video": "span-8",
  "help-rules": "span-7 prepend-1",
  "help-faq": "span-7 prepend-1 last",
  "help-ask": "span-15 prepend-9 last",
}

CSS_CLASSES = {
  "landing-button": "ui-button ui-widget ui-corner-all ui-state-active",
  
  "prizes-add-button": "ui-button ui-state-default ui-corner-all",
  "prizes-remove-button": "ui-button ui-state-error ui-corner-all",
  "prizes-disabled-button": "ui-button ui-state-disabled ui-corner-all",
  
  "widget": "widget ui-corner-all ui-accordion ui-widget ui-accordion-icons",
  "widget-title": "widget-title ui-state-active ui-accordion-header ui-corner-top",
  "widget-body": "widget-body ui-accordion-content ui-helper-reset ui-widget-content ui-corner-bottom ui-accordion-content-active",
  "ui-button": "ui-button ui-state-default ui-corner-all",
}
