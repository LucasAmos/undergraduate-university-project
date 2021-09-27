Feature: As a website user,
            I want to be able to delete a portfolio

  Scenario: Existing portfolio for given name
     Given the application is setup
       And i login with "lucas2" and "test"
       And a portfolio with the name "testportfolio" exists
      When i delete a portfolio called "testportfolio"
      Then "testportfolio" should not appear in the list of portfolios


    delete portfolio with shares in it



