$(function () {
  $('.card-contents').on('click', '.stop-following, .start-following', async function (e) {
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


  $('body').on('click', '.like-btn', async function (e) {
    e.preventDefault()
    console.log("THis event is happening", e.target.closest("a"))
    let response = await axios.post(`/likes/${e.target.closest("a").id}/update`)

    if (response.status === 200) {
      $(e.target).closest("a").toggleClass('likes not-likes')
    }
  });
});