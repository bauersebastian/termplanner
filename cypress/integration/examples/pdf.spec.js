context('Mein Profil', () => {
    beforeEach(() => {

        cy.visit(Cypress.env('loginUrl'))

        // Login-Seite
        cy.get('#id_login').type(Cypress.env('login_name_correct'))
        cy.get('#id_password').type(Cypress.env('login_password_correct'))
        cy.get('.primaryAction').click()
    })

    afterEach(() => {
        cy.get(':nth-child(2) > .nav-item > .nav-link').click()
        cy.get('.btn').click()
    })

    it('(#21) Der PDF-Export sollte vorhanden sein.', () => {
        cy.get(':nth-child(3) > .col > .btn').contains('PDF Export der Terminplanung')
    })

})
