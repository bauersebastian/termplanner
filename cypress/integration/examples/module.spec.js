context('Module', () => {
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


    it('Es sollten neue Module hinzugefügt werden können.', () => {
        cy.get(':nth-child(2) > .btn').contains('Modul hinzufügen')
        cy.get(':nth-child(2) > .btn').click()
        cy.wait(100)
        cy.url().should('include', '/semester/add')
    })

    it('Es sollten alle Felder enthalten sein.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#div_id_term > label').contains('Semester')
        cy.get('#div_id_module > label').contains('Modulbezeichnung')
        cy.get('#div_id_points_sl > label').contains('Punkte Studienleistung')
        cy.get('#div_id_points_exam > label').contains('Punkte Klausur')
        cy.get('#div_id_grade > label').contains('Note')
        cy.get('.form-check-label').contains('Erledigt?')
    })

    it('Es soll ein Hilfetext ausgegeben werden, sofern kein Semester ausgewählt wird.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('.btn').click()

        cy.get('#id_term').then(($input) => {
            expect($input[0].validationMessage).to.eq('Wählen Sie ein Element in der Liste aus.')
        })

    })

    it('Es soll ein Hilfetext ausgegeben werden, sofern kein Modul ausgewählt wird.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')

        cy.get('.btn').click()

        cy.get('#id_module').then(($input) => {
            expect($input[0].validationMessage).to.eq('Wählen Sie ein Element in der Liste aus.')
        })
    })

    it('Es soll zwischen Sommer- und Wintersemester unterschieden werden.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').contains('Data Science')
        cy.get('#id_module').contains('Digitale Transformation').should('not.exist')

    })

    it('Gespeicherte Werte sollen korrekt übernommen werden.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').select('Data Science')
        cy.get('#id_points_sl').type(12)
        cy.get('#id_points_exam').type(10)
        cy.get('#id_grade').type(1)

        cy.get('.btn').click()

        cy.get('h2').contains('Data Science')
        cy.get(':nth-child(5) > .col').contains('Belegt im Wintersemester 2020/21')
        // Punkte Studienleistung 
        cy.get('.col > .table > tbody > :nth-child(1) > :nth-child(2)').contains('12,0')

        // Punkte Klausur 
        cy.get('.col > .table > tbody > :nth-child(2) > :nth-child(2)').contains('10,0')

        // Note
        cy.get('.col > .table > tbody > :nth-child(3) > :nth-child(2)').contains('1,0')


        // Der Löschbutton 
        cy.get('.btn-danger').click()

        // Bestätigungsseite 
        cy.get('p').contains('Bist du sicher, dass du das Modul löschen willst?')
        cy.get('.btn').contains('Löschen bestätigen')
        cy.get('.btn').click()

    })

    it('Die Modulangaben sind enthalten.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').select('Data Science')
        cy.get('#id_points_sl').type(12)
        cy.get('#id_points_exam').type(10)
        cy.get('#id_grade').type(1)

        cy.get('.btn').click()

        cy.get(':nth-child(8) > tbody > :nth-child(1) > :nth-child(1)').contains('Anbieter')
        cy.get(':nth-child(8) > tbody > :nth-child(2) > :nth-child(1)').contains('Beschreibung')
        cy.get(':nth-child(8) > tbody > :nth-child(3) > :nth-child(1)').contains('ECTS')
        cy.get(':nth-child(8) > tbody > :nth-child(4) > :nth-child(1)').contains('Anteil WiWi')
        cy.get(':nth-child(8) > tbody > :nth-child(5) > :nth-child(1)').contains('Anteil Informatik')
        cy.get(':nth-child(8) > tbody > :nth-child(6) > :nth-child(1)').contains('Anteil Wirtschaftsinformatik')
        cy.get(':nth-child(8) > tbody > :nth-child(7) > :nth-child(1)').contains('Anteil Schlüsselkompetenzen')

        cy.get(':nth-child(8) > tbody > :nth-child(1) > :nth-child(2)').contains('Prof. Dr. Tim Weitzel Universität Bamberg')
        cy.get(':nth-child(8) > tbody > :nth-child(2) > :nth-child(2)').contains('Lehrformen & Medienformen: Für dieses Modul steht eine internetbasierte Lernumgebung für die Durchführung der Lehr-/Lernprozesse und der Lernunterstützungsprozesse zur Verfügung. Dabei erfolgt die Betreuung der Studierenden durch die Lehrenden über asynchrone (Foren, E-Mail) und synchrone (Chat, Telefon, Online-Konferenzen) Kommunikationswerkzeuge. Diese stehen auch für die Kommunikation der Studierenden untereinander zur Verfügung.')
        cy.get(':nth-child(8) > tbody > :nth-child(3) > :nth-child(2)').contains(5)
        cy.get(':nth-child(8) > tbody > :nth-child(4) > :nth-child(2)').contains(5)
        cy.get(':nth-child(8) > tbody > :nth-child(5) > :nth-child(2)').contains(55)
        cy.get(':nth-child(8) > tbody > :nth-child(6) > :nth-child(2)').contains(35)
        cy.get(':nth-child(8) > tbody > :nth-child(7) > :nth-child(2)').contains(5)


        // Der Löschbutton 
        cy.get('.btn-danger').click()

        // Bestätigungsseite 
        cy.get('p').contains('Bist du sicher, dass du das Modul löschen willst?')
        cy.get('.btn').contains('Löschen bestätigen')
        cy.get('.btn').click()

    })

    it('Module sollen gelöscht werden können.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').select('Data Science')
        cy.get('#id_points_sl').clear()
        cy.get('#id_points_sl').type(12)
        cy.get('#id_points_sl').clear()
        cy.get('#id_points_exam').type(10)
        cy.get('#id_grade').type(1)
        cy.get('.btn').click()

        // Der Löschbutton 
        cy.get('.btn-danger').click()

        // Bestätigungsseite 
        cy.get('p').contains('Bist du sicher, dass du das Modul löschen willst?')
        cy.get('.btn').contains('Löschen bestätigen')
        cy.get('.btn').click()

        //TODO: Ggf. URL aufrufen
    })

    it('Module sollen bearbeitet werden können.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').select('Data Science')
        cy.get('.btn').click()

        // Der Ändern Button
        cy.get(':nth-child(1) > :nth-child(2) > .btn-secondary').click()

        // Ändernseite
        cy.get('#id_points_sl').clear()
        cy.get('#id_points_sl').type(12)
        cy.get('#id_points_exam').clear()
        cy.get('#id_points_exam').type(10)
        cy.get('#id_grade').type(1)
        cy.get('.btn').click()

        cy.get('h2').contains('Data Science')
        cy.get(':nth-child(5) > .col').contains('Belegt im Wintersemester 2020/21')

        // Punkte Studienleistung 
        cy.get('.col > .table > tbody > :nth-child(1) > :nth-child(2)').contains('12,0')

        // Punkte Klausur 
        cy.get('.col > .table > tbody > :nth-child(2) > :nth-child(2)').contains('10,0')

        // Note
        cy.get('.col > .table > tbody > :nth-child(3) > :nth-child(2)').contains('1,0')

        // Der Löschbutton 
        cy.get('.btn-danger').click()

        // Bestätigungsseite 
        cy.get('p').contains('Bist du sicher, dass du das Modul löschen willst?')
        cy.get('.btn').contains('Löschen bestätigen')
        cy.get('.btn').click()
    })


    it('Als Note darf kein Wert über 5.0 angegeben werden.', () => {
        cy.get(':nth-child(2) > .btn').click()

        cy.get('#id_term').select('Wintersemester 2020/21')
        cy.get('#id_module').select('Data Science')
        cy.get('#id_points_sl').clear()
        cy.get('#id_points_sl').type(12)
        cy.get('#id_points_exam').clear()
        cy.get('#id_points_exam').type(10)
        cy.get('#id_grade').type('5.1')
        cy.get('.btn').click()

        cy.get('#error_1_id_grade').contains('Dieser Wert muss kleiner oder gleich 5.0 sein.')

    })



})
