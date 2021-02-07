/// <reference types="cypress" />

context('Navigation', () => {
    beforeEach(() => {
        cy.visit(Cypress.env('baseUrl'))
    })

    it('(#15) Alle Navigationspunkte sollen enthalten sein.', () => {
        cy.get('.active > .nav-link').contains('Startseite')
        cy.get('#sign-up-link').contains('Registrieren')
        cy.get('#log-in-link').contains('Anmelden')
    })

    it('(#16) Es sollen alle Footer-Links enthalten sein.', () => {
        cy.get('[href="/imprint/"]').contains('Impressum')
        cy.get('[href="/privacy/"]').contains('Datenschutz')
        cy.get('[target="_blank"]').contains('Handbuch')
    })

    it('(#17) Der Impressumslink soll funktionsfähig sein.', () => {
        cy.get('[href="/imprint/"]').click()
        cy.get('h1').contains('Impressum')
        cy.url().should('include', '/imprint')
    })

    it('(#18) Der Datenschutzlink soll funktionsfähig sein.', () => {
        cy.get('[href="/privacy/"]').click()
        cy.get('h1').contains('Datenschutz')
        cy.url().should('include', '/privacy')
    })

    it('(#19) Der Handbuchlink soll funktionsfähig sein.', () => {
        cy.get('.text-muted > [target="_blank"]').should('have.attr', 'href', 'https://termplanner.readthedocs.io/de/latest/index.html')
    })


    it('(#20) Alle Navigationspunkte sollen nach dem Login enthalten sein.', () => {
        cy.visit(Cypress.env('loginUrl'))

        cy.get('#id_login').type(Cypress.env('login_name_correct'))
        cy.get('#id_password').type(Cypress.env('login_password_correct'))
        cy.get('.primaryAction').click()

        cy.get('.mr-auto > :nth-child(1) > .nav-link').contains('Dashboard')
        cy.get(':nth-child(2) > .nav-link').contains('Mein Profil')
        cy.get(':nth-child(2) > .nav-item > .nav-link').contains('Abmelden')

        cy.get(':nth-child(2) > .nav-item > .nav-link').click()
        cy.get('.btn').click()
    })

})
