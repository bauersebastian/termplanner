context('Termine', () => {
    beforeEach(() => {
        cy.visit(Cypress.env('loginUrl'))

        // Login-Seite
        cy.get('#id_login').type(Cypress.env('login_name_correct'))
        cy.get('#id_password').type(Cypress.env('login_password_correct'))
        cy.get('.primaryAction').click()

        cy.get(':nth-child(2) > .nav-link').click()
    })

    afterEach(() => {
        cy.get(':nth-child(2) > .nav-item > .nav-link').click()
        cy.get('.btn').click()
    })

    it('(#22) Der Button Passwort ändern sollte vorhanden sein.', () => {
        cy.contains('Passwort ändern').click()
        cy.contains('Passwort ändern')
        cy.get('#div_id_oldpassword > .requiredField').contains('Aktuelles Passwort*')
        cy.get('#div_id_password1 > .requiredField').contains('Neues Passwort*')
        cy.get('#div_id_password2 > .requiredField').contains('Neues Passwort (Wiederholung)*')
    })

    it('(#23) Der Button Name ändern sollte vorhanden sein und die entsprechenden Felder.', () => {
        cy.contains('Mein Profil').click()
        cy.contains('Name ändern').click()
        cy.contains(Cypress.env('login_name_correct'))
        cy.contains('Benutzerprofil ändern')
        cy.contains('Dein aktueller Benutzername lautet: ' + Cypress.env('login_name_correct'))
        cy.get('label').contains('Name des Benutzers')
        cy.get('.btn').contains('Benutzer ändern')
    })

    it('(#24) Der Button E-Mailadresse ändern sollte vorhanden sein.', () => {
        cy.contains('E-Mail ändern').click()
        cy.contains('Folgende E-Mail-Adressen sind mit diesem Konto verknüpft:')
        cy.get('.primary_email').contains('Bestätigt / Primär')
        cy.get(':nth-child(2) > .secondaryAction').contains('Als primäre Adresse festlegen')
        cy.get(':nth-child(3) > .secondaryAction').contains('Bestätigungs-Mail nochmal verschicken')
        cy.get('.primaryAction').contains('Entfernen')
        cy.get('.add_email > .btn').contains('E-Mail hinzufügen')
    })
})