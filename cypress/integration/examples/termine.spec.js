context('Termine', () => {
    beforeEach(() => {
        cy.visit(Cypress.env('loginUrl'))

        // Login-Seite
        cy.get('#id_login').type(Cypress.env('login_name_correct'))
        cy.get('#id_password').type(Cypress.env('login_password_correct'))
        cy.get('.primaryAction').click()
    })

    const add_module = (() => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').select('Data Science')
        cy.get('#id_points_sl').clear()
        cy.get('#id_points_sl').type(12)
        cy.get('#id_points_sl').clear()
        cy.get('#id_points_exam').type(10)
        cy.get('#id_grade').type(1)
        cy.get('.btn').click()
    })

    const delete_module = (() => {
        // Der Löschbutton 
        cy.get(':nth-child(1) > .btn').click()

        // Bestätigungsseite 
        cy.get('p').contains('Bist du sicher, dass du das Modul löschen willst?')
        cy.get('.btn').contains('Löschen bestätigen')
        cy.get('.btn').click()
    })

    it('Angaben sollen in die Übersicht korrekt übernommen werden.', () => {
        add_module()

        cy.get(':nth-child(3) > :nth-child(2) > .btn').click()

        cy.get('#id_title').type('Testtermin')
        cy.get('#id_note').type('Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.')
        cy.get('#id_start_date').click()
        cy.wait(61000)
        cy.get('#id_end_date').click()

        cy.get('.btn-primary').click()

        cy.wait(4000)
        cy.get('tbody > tr > :nth-child(3)').contains('Skriptbearbeitung')
        cy.get('tbody > tr > :nth-child(4)').contains('Testtermin')

    })

    it('Der Button zum Hinzufügen von Terminen soll vorhanden sein.', () => {
        add_module()

        cy.get(':nth-child(3) > :nth-child(2) > .btn').contains('Termin hinzufügen')
        cy.get(':nth-child(3) > :nth-child(2) > .btn').click()
    })


    it('Alle Angaben zum Hinzufügen von Terminen sollen vorhanden sein.', () => {
        add_module()

        cy.get(':nth-child(3) > :nth-child(2) > .btn').click()

        cy.get('#div_id_title').contains('Titel')
        cy.get('#div_id_note').contains('Notiz')
        cy.get('form > :nth-child(4)').contains('Startzeitpunkt')
        cy.get(':nth-child(5) > label').contains('Endezeitpunkt')
        cy.get('.form-check-label').contains('Erledigt')
        cy.get('#div_id_event_type > .requiredField').contains('Art des Ereignisses')

        // Dropdownfelder
        cy.get('#id_event_type').contains('Skriptbearbeitung')
        cy.get('#id_event_type').contains('Studienleistung')
        cy.get('#id_event_type').contains('Klausur Block A')
        cy.get('#id_event_type').contains('Klausur Block B')
        cy.get('#id_event_type').contains('Klausur Block C')
        cy.get('#id_event_type').contains('Abstimmungstermin')

    })
})