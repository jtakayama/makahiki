"""
page_settings.py
This file contains settings for the page layouts.
"""

###############################################
# PAGE LAYOUT GLOBALs
###############################################
WIDTHS = {
    "DEFAULT": 1024,
    "LARGE": 2048,
    "TABLET_PORTRAIT": 500,
    "TABLET_LANDSCAPE": 768,
    "PHONE_PORTRAIT": 240,
    "PHONE_LANDSCAPE": 320,
    }

###############################################
# PAGE LAYOUT SETTINGS
###############################################
# each page's layout is defined in a dictionary with the page name as the key, and another
# dictionary as the layout settings for the page. The settings dictionary includes keys such as
# "PAGE_TITLE", "BASE_TEMPLATE", and "LAYOUTS". LAYOUTS is another dictionary to include layouts
# for different device widths defined above.
# An LAYOUTS example is:
#    { "<WIDTHS>" : ( (("row1_widget1", "40%"), ("row1_widget2", "60%")),
#                     ("row2_widget", "100%") ) }
PAGE_SETTINGS = {
    # home page
    "home":
            {"PAGE_TITLE": "Home",
             "BASE_TEMPLATE": "logged_in_base.html",
             "LAYOUTS":
                     {"DEFAULT":
                          (
                              ("notifications", "100%"),
                              ("quests", "100%"),
                              ("home", "100%"),
                          ),
                      "PHONE_PORTRAIT":
                          (
                              ("home", "100%"),
                          ),
                     },
             },

    # help page
    "help":
        {"PAGE_TITLE": "Help",
         "BASE_TEMPLATE": "logged_in_base.html",
         "LAYOUTS":
                 {"DEFAULT":
                      (
                          ("notifications", "100%"),
                          ("quests", "100%"),
                          (("help_intro", "50%"), ("help_rule", "50%"), ),
                          (("help_faq", "50%"), ("ask_admin", "50%"),),

                      ),
                  "PHONE_PORTRAIT":
                      (
                          ("help_intro", "100%"),
                          ("help_faq", "100%"),
                          ("help_rule", "100%"),
                          ("ask_admin", "100%"),
                      ),
                 },
         },

    # actions page
    "actions":
        {"PAGE_TITLE": "Actions",
         "BASE_TEMPLATE": "logged_in_base.html",
          "LAYOUTS":
              {"DEFAULT":
                 (
                  ("notifications", "100%"),
                  ("quests", "100%"),
                  (("upcoming_events", "40%"), ("smartgrid", "60%"), ("scoreboard", "40%"),),
                 ),
               "PHONE_PORTRAIT":
                 (("upcoming_events", "100%"),
                  ("smartgrid", "100%"),
                  ("scoreboard", "100%"),
                 ),
              },
        },

    # profile page
    "profile":
        {"PAGE_TITLE": "Profile",
          "BASE_TEMPLATE": "logged_in_base.html",
          "LAYOUTS":
              {"DEFAULT":
                (
                  ("profile", "100%"),
                  ("badges", "100%"),
                ),
                "PHONE_PORTRAIT":
                (
                  ("profile", "100%"),
                  ("badges", "100%"),
                ),
              },
        },

    # news page
    "news":
        {"PAGE_TITLE": "News",
          "BASE_TEMPLATE": "logged_in_base.html",
          "LAYOUTS":
              {"DEFAULT":
                (
                  ("notifications", "100%"),
                  ("quests", "100%"),
                  (("upcoming_events", "50%"), ("news", "50%"), ("wallpost", "50%"), ),
                ),
                "PHONE_PORTRAIT":
                (
                  ("wallpost", "100%"),
                  ("news", "100%"),
                  ("upcoming_events", "100%"),
                ),
              },
        },

    # energy page
    "energy":
        {"PAGE_TITLE": "Energy",
          "BASE_TEMPLATE": "logged_in_base.html",
          "LAYOUTS":
              {"DEFAULT":
                (
                    ("notifications", "100%"),
                    ("quests", "100%"),
                    (("energy_power_meter", "35%"), ("energy_goal", "65%"), ("energy_scoreboard", "35%"), ("wallpost", "65%"),),

                ),
                "PHONE_PORTRAIT":
                (
                  ("energy_power_meter", "100%"),
                  ("energy_goal", "100%"),
                  ("energy_scoreboard", "100%"),
                  ("wallpost", "100%"),
                ),
              },
        },

    # prizes page
    "prizes":
        {"PAGE_TITLE": "Prizes",
          "BASE_TEMPLATE": "logged_in_base.html",
          "LAYOUTS":
              {"DEFAULT":
                (
                  ("prizes", "100%"),
                ),
                "PHONE_PORTRAIT":
                (
                  ("prizes", "100%"),
                ),
              },
        },
    # canopy page
    "canopy":
            {"PAGE_TITLE": "Canopy",
             "BASE_TEMPLATE": "logged_in_base.html",
             "LAYOUTS":
                     {"DEFAULT":
                          (
                              ("canopy", "100%"),
                              ),
                      "PHONE_PORTRAIT":
                          (
                              ("canopy", "100%"),
                              ),
                      },
             },
}
