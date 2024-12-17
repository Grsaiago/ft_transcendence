import AbstractView from "./abstractView.js";

export default class Profile extends AbstractView {
    constructor() {
        super();
        this.setTitle("Profile");

        this.handleFriendChange = this.handleFriendChange.bind(this);
        this.updateFriend = this.updateFriend.bind(this);
        this.handleTabSwitch = this.handleTabSwitch.bind(this);
        this.handleSearchEnterKey = this.handleSearchEnterKey.bind(this);
        this.handleUserSearch = this.handleUserSearch.bind(this);
    }

    async getHtml() {
        try {
            const response = await fetch('/friends/', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const html = await response.text();
            console.log('Friends html fetched. Returning...');
            return html;
        }
        catch(error) {
            console.error('Failed to fetch page: ', error);
            return "<p>Error loading login page</p>";
        }
    }

    bindUIEventHandlers() {
        console.log('Loading friends event handlers...');

        //select first friend and set eventlistener for change friends
        const friendList = document.querySelectorAll("[data-friend]");
        if (friendList.length > 0) {
            this.selectFirstFriend(friendList[0]);
            console.log(friendList[0]);
        } else {
            console.warn("No friends found")
        }

        friendList.forEach(friend => {
            friend.addEventListener("click", this.handleFriendChange);
        });

        //add click event for switch tabs between friends and search
        const titleFriends = document.querySelector("#title-friends-friend");
        const titleSearch = document.querySelector("#title-friends-search");
        titleFriends.addEventListener("click", this.handleTabSwitch);
        titleSearch.addEventListener("click", this.handleTabSwitch);

        //search events
        const searchBarInput = document.getElementById('search-input');
        searchBarInput.addEventListener('keydown', this.handleSearchEnterKey);

        const friendsBarInput = document.getElementById('friends-input');
        friendsBarInput.addEventListener('keydown', this.handleSearchEnterKey);
    }
    
    removeUIEventHandlers() {
        console.log('Removing friends event handlers...');
        
        const friendList = document.querySelectorAll("[data-friend]");
        friendList.forEach(friend => {
            friend.removeEventListener("click", this.handleFriendChange);
        });

        const titleFriends = document.querySelector("#title-friends-friend");
        const titleSearch = document.querySelector("#title-friends-search");
        titleFriends.removeEventListener("click", this.handleTabSwitch);
        titleSearch.removeEventListener("click", this.handleTabSwitch);
    }

    handleSearchEnterKey(event, tab) {
        if (event.key === 'Enter') {
            if (event.currentTarget.id === 'friends-input') {
                this.handleFriendsSearch();
            } else {
                this.handleUserSearch();
            }
        }
    }

    handleUserSearch() {
        const messageInputDom = document.getElementById('search-input');

        if (!messageInputDom) {
            console.error('Message input field not found.');
            return;
        }

        const message = messageInputDom.value;

        console.log('Sending message: ', message);

        if (!message) {
            return;
        }

        messageInputDom.value = '';

        this.renderUserSearch(this.searchUsers());
    }

    handleFriendsSearch() {
        const messageInputDom = document.getElementById('friends-input');

        if (!messageInputDom) {
            console.error('Message input field not found.');
            return;
        }

        const message = messageInputDom.value;

        console.log('Sending message: ', message);

        if (!message) {
            return;
        }

        messageInputDom.value = '';

        this.renderFriendsList(this.getFriendsList());
    }

    getFriendsList() {
        //endpoint to get friends list
        var friends = [];
        return friends;
    }

    searchUsers() {
        //endpoint to get search results
        var users = [];
        return users;
    }

    renderFriendsList(friends) {
        //render friends list based on friends array
        console.log("rendering friends list");
    }

    renderUserSearch(users) {
        //render search results based on results array
        console.log("rendering user search results");
    }

    handleTabSwitch(event) {
        const tab = event.target.textContent.trim().toLowerCase();
        this.toggleTabs(tab);
    }

    toggleTabs(tab) {
        const divFriend = document.querySelector('.div-friend');
        const divSearch = document.querySelector('.div-search');
        const titleFriends = document.querySelector("#title-friends-friend");
        const titleSearch = document.querySelector("#title-friends-search");
    
        if (tab === 'friends') {
            divFriend.style.display = 'block';
            divSearch.style.display = 'none';
            titleSearch.classList.remove('selected'); 
            titleFriends.classList.add('selected');
            console.log("change tab to friends");
            
            this.unhighlightPreviousFriend();

            setTimeout(() => {
                const friendList = document.querySelectorAll("[data-friend]");
                if (friendList.length > 0) {
                    this.selectFirstFriend(friendList[0]);
                }
            }, 0); 
        } else if (tab === 'search') {
            divFriend.style.display = 'none';
            divSearch.style.display = 'block';
            titleFriends.classList.remove('selected');
            titleSearch.classList.add('selected');
            console.log("change tab to search");

            this.unhighlightPreviousFriend();

            const firstSearchFriend = document.querySelector(".div-search [data-friend]");
            if (firstSearchFriend) {
                this.selectFirstFriend(firstSearchFriend);
            }
        }
    }
    
    selectFirstFriend(friendDiv) {
        this.currentFriend = friendDiv.getAttribute('data-friend');
        this.highlightSelectedFriend(friendDiv);
        this.updateFriend(friendDiv);
    }

    handleFriendChange(event) {
        this.unhighlightPreviousFriend();
        const friendElement = event.currentTarget;

        if (!friendElement) {
            console.error("Friend element not found");
            return;
        }

        const friendId = friendElement.dataset.friend;
        if (!friendId) {
            console.error("Friend ID is missing in dataset");
            return;
        }

        this.highlightSelectedFriend(friendElement);
        this.updateFriend(friendElement);
       
    }
    
    updateFriend(friendElement) {
        const friendId = friendElement.dataset.friend;
        const friendName = friendElement.dataset.friend;
        
        const profileIdElement = document.querySelector("[friend-id]");
        const profileNameElement = document.querySelector("[friend-name]");
    
        console.log(profileIdElement, profileNameElement);
    
        if (profileIdElement) {
            profileIdElement.textContent = friendName;
        } else {
            console.error("Profile ID element not found")
        }
        
        if (profileNameElement) {
            profileNameElement.textContent = friendName;
        } else {
            console.error("Profile name element not found")
        }
    }

    highlightSelectedFriend(eventTarget) {
        const outerDiv = eventTarget.closest('.friend');
        if (outerDiv)
            outerDiv.classList.add('selected');
    }

    unhighlightPreviousFriend() {
        const selectedFriend = document.querySelector('.friend.selected');
        if (selectedFriend) {
            selectedFriend.classList.remove('selected');
        }
    }

}