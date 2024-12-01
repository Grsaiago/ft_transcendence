import AbstractView from "./abstractView.js";

export default class Profile extends AbstractView {
    constructor() {
        super();
        this.setTitle("Profile");

        this.handleFriendChange = this.handleFriendChange.bind(this);
        this.updateFriend = this.updateFriend.bind(this);
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

        const friendList = document.querySelectorAll("[data-friend]");
        this.selectFirstFriend(friendList[0]);
        console.log(friendList[0]);
        friendList.forEach(friend => {
            friend.addEventListener("click", this.handleFriendChange);
        });
        this.updateFriend(friendList[0]);
    }

    
    removeUIEventHandlers() {
        console.log('Removing friends event handlers...');
        
        const friendList = document.querySelectorAll("[data-friend]");
        friendList.forEach(friend => {
            friend.removeEventListener("click", this.handleFriendChange);
        });
    }
    
    selectFirstFriend(friendDiv) {
        this.currentFriend = friendDiv.getAttribute('data-friend');
        this.highlightSelectedFriend(friendDiv);
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