function confirmDelete(event) {
    event.preventDefault(); // stop form from submitting immediately
    const confirmed = confirm("Are you sure you want to delete this post?");
    if (confirmed) {
      event.target.submit(); // submit the form if user clicked "Yes"
    }
    return false;
  }
