/*
    payment 

*/

var stripe_public_key = $('#id_stripe_public_key').text().slice(1,-1); //Gets the stripe key 
var client_secret = $('#id_client_secret').text().slice(1,-1); //Gets the client key
var stripe = Stripe(stripe_public_key); // stores stripe
var stripe_elements = stripe.elements();// stores all the elements



var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};
var card = stripe_elements.create('card', {style: style}); // stores a card element
card.mount('#card');
card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});