document.addEventListener('DOMContentLoaded', function() {
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('/emails/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => { throw new Error(text); });
        }
        return response.json();
    })
    .then(result => {
        console.log('Email sent:', result);
        setTimeout(() => load_mailbox('sent'), 200);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Не вдалося відправити email. Подробиці в консолі.');
    });
});
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(replyEmail) {   // можна назвати як хочеш

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Clear out composition fields
    if (replyEmail) {
        document.querySelector('#compose-recipients').value = replyEmail.sender || '';
    } else {
        document.querySelector('#compose-recipients').value = '';
    }

    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
    // Показуємо emails-view і ховаємо compose
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    // Очищаємо тільки вміст, але залишаємо контейнер
    const emailsView = document.querySelector('#emails-view');
    emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

    // Завантажуємо листи для будь-якої mailbox
    fetch(`/emails/${mailbox}`)
        .then(response => response.json())
        .then(emails => {
        emails.forEach(email => {
    const div = document.createElement('div');
    div.className = 'email-item';

    let email_status = email.archived === true ? 'Dearchive' : 'Archive';

    if (mailbox === 'sent') {
        div.innerHTML = `
            To: <strong>${email.recipients.join(', ')}</strong>
            ${email.subject}
            <span style="float:right;">${email.timestamp}</span>
        `;
    } else {
        div.innerHTML = `
            <strong>${email.sender}</strong>
            ${email.subject}
            <span style="float:right;">${email.timestamp}</span>
            <button class="archive_button" style="float:right;">${email_status}</button>
        `;
    }

    // Фон для непрочитаних
    if (!email.read) {
        div.style.backgroundColor = 'lightgrey';
    }

    // Клік по всьому листі (відкрити email)
    div.addEventListener('click', () => load_email(email.id));

    // === ВИПРАВЛЕНО: Архівна кнопка ===
    const button = div.querySelector('.archive_button');
    if (button) {   // щоб не падало для sent
        button.addEventListener('click', (event) => {
            event.stopPropagation();   // важливо! щоб не відкривався email

            const newArchived = !email.archived;

            fetch(`/emails/${email.id}`, {
                method: 'PUT',
                body: JSON.stringify({ archived: newArchived })
            })
            .then(response => {
                if (response.ok) {
                    // Видаляємо поточний рядок (можна також оновити текст кнопки)
                    div.remove();

                    // Якщо хочеш оновити весь mailbox автоматично:
                    // load_mailbox(mailbox);
                }
            })
            .catch(error => console.error('Error archiving email:', error));
        });
    }

    emailsView.appendChild(div);
});


            if (emails.length === 0) {
                const p = document.createElement('p');
                p.textContent = 'No emails in this mailbox.';
                emailsView.appendChild(p);
            }
        })
        .catch(error => console.error('Error loading mailbox:', error));
}

function load_email(email_id) {
    document.querySelector('#emails-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';

    const emailsView = document.querySelector('#emails-view');
    emailsView.innerHTML = '';

    fetch(`/emails/${email_id}`)
        .then(response => response.json())
        .then(email => {
            const div = document.createElement('div');
            div.className = 'email-text';
            div.innerHTML = `
                <strong>${email.sender}</strong><br>
                ${email.subject}<br>
                <span>${email.timestamp}</span><br><br>
                ${email.body}
                <button class="reply_button">reply</button>
            `;
            emailsView.appendChild(div);

            const button = div.querySelector('.reply_button');
            button.addEventListener('click', ()=>{
                compose_email(email);
            })
        });
        fetch(`/emails/${email_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    read: true
                })
        })
}
