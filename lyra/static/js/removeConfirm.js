window.onload = () => {
  const removeButton = document.getElementById('remove');
  const modal = document.getElementById('modal');
  const backButton = document.getElementById('back');

  removeButton.onclick = () => {
    modal.classList.add('is-active');
  }

  backButton.onclick = () => {
    modal.classList.remove('is-active');
  }

}
