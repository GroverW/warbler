$(function() {
  $('.card-contents').on('click', '.stop-following', async function(e) {
    e.preventDefault()

    let response = await axios.post(`/users/stop-following/${e.target.id}`)

    if(response.status === 200) {
      $(e.target).toggleClass('start-following stop-following btn-primary btn-outline-primary')
      $(e.target).text('Follow')
    }

  })

  $('.card-contents').on('click', '.start-following', async function(e) {
    e.preventDefault()

    let response = await axios.post(`/users/follow/${e.target.id}`)
    
    if(response.status === 200) {
      $(e.target).toggleClass('start-following stop-following btn-primary btn-outline-primary')
      $(e.target).text('Unfollow')
    }

  })
});