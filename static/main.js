$(function () {
  $('body').on('click', '.stop-following', async function (e) {
    e.preventDefault()

    let response = await axios.post(`/users/stop-following/${e.target.id}`)

    if (response.status === 200) {
      $(e.target).toggleClass('start-following stop-following btn-primary btn-outline-primary')
      $(e.target).text('Follow')
    }
  })

  $('body').on('click', '.start-following', async function (e) {
    e.preventDefault()

    let response = await axios.post(`/users/follow/${e.target.id}`)

    if (response.status === 200) {
      $(e.target).toggleClass('start-following stop-following btn-primary btn-outline-primary')
      $(e.target).text('Unfollow')
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