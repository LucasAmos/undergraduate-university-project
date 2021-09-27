Feature: As a website user,
            I want to be able to add a portfolio

  Scenario: Successfully added a new portfolio
     Given the application is setup
     And   i login with "lucas2" and "test"
      When i add a portfolio called "portfolio1"
      Then i should see the alert "Added portfolio 'portfolio1'"

  Scenario: Existing portfolio for given name
     Given the application is setup
       And i login with "lucas2" and "test"
       And a portfolio with the name "portfolio1" exists
      When i add a portfolio called "portfolio1"
      Then i should see the error "A portfolio with that name already exists"

  Scenario: Existing portfolio for given name except for different letter case
     Given the application is setup
       And i login with "lucas2" and "test"
       And a portfolio with the name "portfolio1" exists
      When i add a portfolio called "Portfolio1"
      Then i should see the error "A portfolio with that name already exists"

  Scenario: Portfolio name contains invalid non-alphanumeric characters
     Given the application is setup
     And   i login with "lucas2" and "test"
      When i add a portfolio called "Test``¬¬|||"
      Then i should see the error "The portfolio name must contain only letters and numbers"

