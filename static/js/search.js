document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('searchButton')

    // 검색 기능
    async function search() {
        const searchText = searchInput.value.toLowerCase()
        // 최소 2글자부터 검색
        if (searchText.length > 1 || searchText.length===0) {
            // redirect
            window.location.href = `/?search=${encodeURIComponent(searchText)}`
            return
        }

        alert('검색어가 너무 짧습니다.')
    }

    // 이벤트 리스너 등록
    searchButton.addEventListener('click', search)
})