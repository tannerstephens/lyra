window.onload = () => {
  const moreButton = document.getElementById('more');
  const loader = document.getElementById('loader');
  const noMore = document.getElementById('no-more');

  let page = 2;

  const createElementsFromHTMLString = (HTMLString) => {
    const div = document.createElement('div')
    div.innerHTML = HTMLString.trim();
    return Array.from(div.children);
  };

  const show = (node) => {
    if(node.classList.contains('is-hidden')) {
      node.classList.remove('is-hidden');
    }
  };

  const hide = (node) => {
    if(!node.classList.contains('is-hidden')) {
      node.classList.add('is-hidden');
    }
  };

  moreButton.onclick = () => {
    if(!moreButton.disabled) {
      moreButton.disabled = true;
      hide(moreButton);
      show(loader);
      fetch(`/groups/new/more?page=${page}`)
        .then(resp => resp.text())
        .then(text => createElementsFromHTMLString(text))
        .then(nodes => {
          nodes.map((node) => moreButton.parentNode.insertBefore(node, moreButton));

          if(nodes.length == 10) {
            moreButton.disabled = false;
            show(moreButton);
            page += 1;
          } else {
            show(noMore);
          }
          hide(loader);
        });
    }
  }
}
