// popup.js
chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    var currentTab = tabs[0];
    chrome.tabs.update(currentTab.id, { url: chrome.runtime.getURL('myApp/templates/home.html') });
  });
  