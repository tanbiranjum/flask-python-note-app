function deleteNote(noteId) {
  console.log('Hello')
  fetch('/delete-note', {
    method: 'POST',
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = '/'
  })
}
