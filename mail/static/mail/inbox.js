document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector("#compose-form").addEventListener('submit', post_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_emails(emails) {

  let counter = 1;

  for (const email of emails) {
    const emailCard = `
      <div class="card">
          <div class="card-header">
              ${email.timestamp}
          </div>
          <div class="card-body">
              <h5 class="card-title">${email.subject}</h5>
              <p class="card-text">${email.sender}</p>
              <div class="collapse mb-2" id="collapseExample${counter}">
                <div class="card card-body">
                  ${email.body}
                </div>
              </div>
              <p class="d-inline-flex gap-4">
                <button class="btn btn-primary view" type="button" data-bs-toggle="collapse" data-bs-target="#collapseExample${counter}" aria-expanded="false" aria-controls="collapseExample${counter}">View</button>

                <button class="btn btn-success" id="read${counter}" type="button" data-email-id="${email.id}">
                  ${email.read ? 'Unread' : 'Read' }
                </button>
                
                <button class="btn btn-dark" id="archive${counter}" type="button" data-email-id="${email.id}">
                  ${email.archive ? 'Archived': 'Archive'}
                </button>

              </p>          
          </div>
      </div>
    `
    document.querySelector('#emails-view').insertAdjacentHTML('beforeend', emailCard);

    document.querySelector(`#read${counter}`).addEventListener('click', (e) => read_email(email.id, e.target));
    document.querySelector(`#archive${counter}`).addEventListener('click', (e) => archive_email(email.id, e.target));

    counter++;
  }
}

function read_email(email_id, button) {
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      const newReadState = !email.read;
      fetch(`/emails/${email_id}`, {
        method: "PUT",
        body: JSON.stringify({
          read: newReadState,
        })
      })
      .then(() => {
        button.textContent = newReadState ? 'Unread' : 'Read';
      })
    })
  }

function archive_email(email_id, button) {
  fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
      const newArchiveState = !email.archived  
      fetch(`/emails/${email_id}`, {
          method: "PUT",
          body: JSON.stringify({
            archived: newArchiveState,
          })
        })
        .then(() => {
          button.textContent = newArchiveState ? 'Archived': 'Archive'
        });
    });
}


function load_email_content(email_id) {

  fetch(`/emails/${email_id}`)
  .this(response => response.json)
  .this(email => {
    const emailContent = `
    `
  })

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  switch (mailbox) {
    case 'sent':
      fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => load_emails(emails));
      
      break;
    case 'archive':
      fetch(`/emails/${mailbox}`)
      .then(response => response.json())
      .then(emails => {
        load_emails(emails);
      });
      break;
    default:
      fetch(`/emails/inbox`)
      .then(response => response.json())
      .then(emails => load_emails(emails));
      break;
  }

}

function post_email(e) {
  console.log("post_email")
    // const formData = new FormData(form);
  e.preventDefault();

  const recipients = document.querySelector("#compose-recipients").value;
  
  const subject = document.querySelector("#compose-subject").value;
  
  const body = document.querySelector("#compose-body").value;
  
  fetch('/emails', {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    }),
  })
  .then(response => response.json())
  .then(result => {
    if (result.message) {
      load_mailbox('sent');  // Changed from window.location.href
    } else if (result.error) {
      alert(result.error);
    }
  })  // Added missing closing brace
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to send email');      
  });
}