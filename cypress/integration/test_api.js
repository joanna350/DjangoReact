describe('Test API', function(){
    it('Can access a public API route', function(){
        cy.visit('http://127.0.0.1:8000/api/lead')
        cy.title().should('include', 'Django REST');
        cy.get('form');
        cy.get('input[name="name"]')
            .type("Abla")
            .should("have.value", "Abla");
        cy.get('input[name="email"]')
            .type("Abla@stan.edu")
            .should("have.value", "Abla@stan.edu");
        cy.get('input[name="message"]')
            .type("Mind if I were once hyper?")
            .should("have.value", "Mind if I were once hyper?");
    });
});
