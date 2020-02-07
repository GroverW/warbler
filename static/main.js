$(function () {
  $('.follow-wrapper').on('click', '.stop-following, .start-following', async function (e) {
    e.preventDefault()
    $link = $(e.target)

    let route = $link.hasClass('stop-following') ? 'stop-following' : 'follow';
    let followText = $link.hasClass('stop-following') ? 'Follow' : 'Unfollow';
    
    let response = await axios.post(`/users/${route}/${e.target.id}`)

    if (response.status === 200) {
      $link.toggleClass('start-following stop-following btn-primary btn-outline-primary text-primary text-white')
      $link.text(followText)
    }
  })


  $('.list-group-item').on('click', '.like-btn', async function (e) {
    e.preventDefault()
    let response = await axios.post(`/likes/${e.target.closest("a").id}/update`)

    if (response.status === 200) {
      $(e.target).closest("a").toggleClass('likes not-likes')
    }
  });

  $('.follow-wrapper').on('click', '.stop-blocking, .start-blocking', async function (e) {
    e.preventDefault()
    $link = $(e.target)

    let route = $link.hasClass('stop-blocking') ? 'unblock' : 'block';
    let blockText = $link.hasClass('stop-blocking') ? 'Block' : 'Unblock';

    let response = await axios.post(`/users/${route}/${e.target.id}`)

    if (response.status === 200) {
      $link.toggleClass('start-blocking stop-blocking btn-danger btn-outline-danger text-danger text-white')
      $link.text(blockText)

      if(route === 'block' && $('.follow-btn-lg').first().text() === 'Unfollow') {
        $('.follow-btn-lg').toggleClass('start-following stop-following btn-primary btn-outline-primary text-primary text-white')
        $('.follow-btn-lg').text('Follow')
      }
    }
  })
});