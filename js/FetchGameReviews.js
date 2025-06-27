const PAGE = arguments[0];

async function delay(seconds) {
    return new Promise((resolve) => setTimeout(resolve, seconds * 1000));
}

function extractGameReview(node) {
    function getAuthor() {
        return node.querySelector(".apphub_CardContentAuthorName").childNodes[1].textContent.trim();
    }

    function getDatePosted() {
        let datePosted = node
            .querySelector(".apphub_CardTextContent .date_posted")
            .textContent.trim()
            .split("：")[1];
        if (!datePosted.includes("年")) {
            datePosted = `${new Date().getFullYear()}年${datePosted}`;
        }
        return datePosted.replace(/\s+/g,"");
    }

    function getHelpfulCount() {
        const foundHelpful = node.querySelector(".found_helpful")?.textContent.trim();
        if (foundHelpful.startsWith("尚未有人觉得这篇评测有价值")) {
            return 0;
        }
        if (foundHelpful.startsWith("1 人觉得这篇评测有价值")) {
            return 1;
        }
        return parseInt(/\d+(?= 人觉得这篇评测有价值)/.exec(foundHelpful)[0]);
    }

    function getIsRecommend() {
        const isRecommend = node.querySelector(".title").textContent.trim();
        switch (isRecommend) {
            case "推荐":
                return true;
            case "不推荐":
                return false;
        }
        return "ERROR";
    }

    function getPlayedHours() {
        const playedHours = node.querySelector(".hours")?.textContent.trim();
        return parseFloat(/(?<=总时数 )[\d\.,]+(?= 小时)/.exec(playedHours)[0]);
    }

    function getMainContent() {
        const mainContent = node.querySelector(".apphub_CardTextContent").cloneNode(true);
        const childNodesToRemove = mainContent.querySelectorAll(
            ".date_posted, .received_compensation"
        );
        childNodesToRemove.forEach((c) => c.remove());
        return mainContent.textContent.trim();
    }

    return {
        author: getAuthor(),
        datePosted: getDatePosted(),
        helpfulCount: getHelpfulCount(),
        isRecommend: getIsRecommend(),
        playedHours: getPlayedHours(),
        mainContent: getMainContent(),
    };
}

const gameReviews = [];
const maxRetryTimes = 20;
let retryTimes = 0;

while (true) {
    const pageRoot = document.querySelector(`#page${PAGE}`);
    if (pageRoot == null) {
        window.scrollTo(0, document.body.scrollHeight + 100);
        retryTimes++;
        if (retryTimes > maxRetryTimes) {
            break;
        }
        await delay(0.5);
        continue;
    }

    const apphubCards = pageRoot.querySelectorAll(".apphub_Card.modalContentLink.interactable");
    for (const card of apphubCards) {
        const gameReview = extractGameReview(card);
        gameReviews.push(gameReview);
    }
    break;
}

return gameReviews;
