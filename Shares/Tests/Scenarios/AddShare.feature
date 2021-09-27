Feature: As a website user,
            I want to be able to add a share

  Scenario: Successfully added a new share to a new portfolio
     Given The application is setup
      And  i login with "lucas2" and "test"
      When i add a share with the symbol "GOOG", a quantity of 10, a purchase price of 100 and a portfolio name of "testportfolio"
      Then i should see the alert "Added share 'GOOG'"

  Scenario: Cannot add share to a portfolio if it already contains that share
     Given The application is setup
      And  i login with "lucas2" and "test"
      When i add a share with the symbol "GOOG", a quantity of 10, a purchase price of 100 and a portfolio name of "testportfolio"
      And  the portfolio "testportfolio" already contains a share with the symbol "GOOG"
      Then i should see the error "That share is already in that portfolio"

  Scenario: Can add a share that exists in one portfolio to a different portfolio as long as it does not exist in that portfolio
     Given The application is setup
      And  i login with "lucas2" and "test"
      And  a share with the symbol "GOOG" exists in the portfolio "testportfolio"
      When i create a portfolio called "secondtestportfolio"
      And  i add a share with the symbol "GOOG", a quantity of 10, a purchase price of 100 and a portfolio name of "secondtestportfolio"
      Then i should see the alert "Added share 'GOOG'"
