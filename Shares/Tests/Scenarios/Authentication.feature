Feature: As a website owner,
            I want to secure my website

  Scenario: Successful Login
     Given The application is setup
      When i login with "lucas2" and "test"
      Then i should see the alert "You were logged in"

  Scenario: Incorrect Username
     Given flaskr is setup
      When i login with "nouser" and "test"
      Then i should see the alert "Incorrect username or password"

  Scenario: Incorrect Password
     Given flaskr is setup
      When i login with "lucas2" and "wrongpassword"
      Then  i should see the alert "Incorrect username or password"

  Scenario: Logout
     Given flaskr is setup
     and i login with "admin" and "default"
      When i logout
      Then  i should see the alert "You were logged out"