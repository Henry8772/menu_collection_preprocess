### June 23 2023
 [x] Successfully configured Google vision api to extract text from photos

### June 24 2023
 [x] Complete selenium crawler to crawl a json of restaurant link based on base links
 [x] Complete selenium crawler to crawl menu and receipt photos from the json of restaurant links


### June 25 2023

 [x] Before download, check photo metric to pre-determine if the photo is good
    - Actually, i found out that i have been crawling the wrong resolution, higher resolution can be found in each photo view. 
 [x] Check why 长宁来福士店 can't be downloaded
    - because it doesn;t have menu or receipt page, so i include mix_photos page for this scenarios
 [x] Crawler will not download duplicated files and store progress in blue-frog-menu.json
 

### June 26 2023
 [ ] Websire forcibly shutdown the connection, need to fake normal user behaviour and using VPN to hide identity if needed
 [ ] use the information online, reconstruct the chinese monolingual menu
 [ ] Then use the monolingual data, align with bilingual menus to reconstruct the bilingual menu
 [ ] Crawler able to start from where it left of