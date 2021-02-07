context('Login', () => {
  beforeEach(() => {
    cy.visit(Cypress.env('loginUrl'))
  })


  it('Der Login und Logout sollen funktionsfähig sein.', () => {

    // Login-Seite
    cy.get('#id_login').type(Cypress.env('login_name_correct'))
    cy.get('#id_password').type(Cypress.env('login_password_correct'))
    cy.get('.primaryAction').click()

    // Check ob der Login erfolgreich war 
    cy.url().should('include', '/semester')
    cy.get('.alert').contains('Erfolgreich')
    cy.getCookie('sessionid').should('exist')

    // Logout 
    cy.get(':nth-child(2) > .nav-item > .nav-link').click()
    cy.get('h1').contains('Abmelden')
    cy.get('p').contains('Bist du sicher, dass du dich abmelden möchtest?')
    cy.get('.btn').contains('Abmelden')
    cy.get('.btn').click()
    cy.getCookie('sessionid').should('not.exist')
    cy.get('.alert').contains('Du hast dich abgemeldet.')
  })

  it('Es soll ein Hilfetext ausgegeben werden, sofern kein Benutzername enthalten ist.', () => {

    // Login-Seite
    cy.get('#id_password').type(Cypress.env('login_password_wrong'))
    cy.get('.primaryAction').click()
    cy.get('#id_login').then(($input) => {
      expect($input[0].validationMessage).to.eq('Füllen Sie dieses Feld aus.')
    })
  })

  it('Es soll ein Hilfetext ausgegeben werden, sofern kein Passwort eingegeben wurde.', () => {

    // Login-Seite
    cy.get('#id_login').type(Cypress.env('login_name_wrong'))
    cy.get('.primaryAction').click()
    cy.get('#id_password').then(($input) => {
      expect($input[0].validationMessage).to.eq('Füllen Sie dieses Feld aus.')
    })
  })

  it('Es soll ein Hinweistext ausgegeben werden, sofern das Passwort falsch eingegeben wurde.', () => {

    // Login-Seite
    cy.get('#id_login').type(Cypress.env('login_name_wrong'))
    cy.get('#id_password').type(Cypress.env('login_password_wrong'))
    cy.get('.primaryAction').click()

    // Check ob die Validierung angezeigt wird
    cy.get('.m-0 > li').contains('Der Anmeldename und/oder das Passwort sind leider falsch.')
    cy.getCookie('sessionid').should('not.exist')
  })


})

