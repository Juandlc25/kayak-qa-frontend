@regression_tests

Feature: Validate element created dropdown column

  Scenario: Navigate to the Kayak home page and validate principal elements
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    And The page "should" contain the next elements
      | name                   | type   |
      | name_tag               | input  |
      | name_dropdown_column   | input  |
      | search_tag             | input  |

  Scenario: Validate URL of Home page
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    And The url page should be equal to the next "https://www.kayak.com" url

  Scenario Outline: Navigate between countries and validate the URL
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    When I navigate to the "<url>" URL
    Then The url page should be equal to the next "<url>" url

  Examples:
    | url                       |
    | https://www.kayak.com.my/ |
    | https://www.kayak.com.pr/ |
    | https://www.kayak.com.br/ |

  Scenario Outline: Navigate through the main menu and validate the pages
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    When I click on the "<dropdown>" "dropdown"
    When I click on the "<option>" "option"
    Then The url page should be equal to the next "<url>" url

  Examples:
    | dropdown             | option                | url                                |
    | menu                 | flights_dropdown_menu | https://www.kayak.com.co/flights   |
    | menu                 | stays_dropdown_menu   | https://www.kayak.com.co/stays     |
    | menu                 | cars_dropdown_menu    | https://www.kayak.com.co/cars      |
    | menu                 | blog_dropdown_menu    | https://www.kayak.com.co/news/      |
    | menu                 | direct_dropdown_menu    | https://www.kayak.com.co/direct      |
    | menu                 | trips_dropdown_menu    | https://www.kayak.com.co/trips      |
