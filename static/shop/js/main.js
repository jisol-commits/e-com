const navToggle = document.querySelector("[data-nav-toggle]");
const nav = document.querySelector("[data-nav]");
const cartCount = document.querySelector("[data-cart-count]");
let cartItems = 0;

function fallbackImage(title) {
  const safeTitle = (title || "Neo China").replace(/[&<>"']/g, "");
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="900" height="1100" viewBox="0 0 900 1100">
      <defs>
        <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0" stop-color="#21180d"/>
          <stop offset="0.52" stop-color="#090807"/>
          <stop offset="1" stop-color="#000000"/>
        </linearGradient>
        <linearGradient id="gold" x1="0" x2="1">
          <stop offset="0" stop-color="#f3d78a"/>
          <stop offset="1" stop-color="#a77925"/>
        </linearGradient>
      </defs>
      <rect width="900" height="1100" fill="url(#bg)"/>
      <circle cx="450" cy="370" r="210" fill="none" stroke="url(#gold)" stroke-width="22" opacity="0.75"/>
      <rect x="260" y="250" width="380" height="240" rx="26" fill="#0f0f0f" stroke="url(#gold)" stroke-width="16"/>
      <path d="M310 545h280M330 595h240M350 645h200" stroke="url(#gold)" stroke-width="18" stroke-linecap="round"/>
      <text x="450" y="790" text-anchor="middle" fill="#f1d486" font-family="Arial, sans-serif" font-size="54" font-weight="800">Neo China</text>
      <text x="450" y="860" text-anchor="middle" fill="#b9ad98" font-family="Arial, sans-serif" font-size="30">${safeTitle}</text>
    </svg>`;
  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

function showToast(message) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add("show");
  window.setTimeout(() => toast.classList.remove("show"), 1800);
}

if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

document.querySelectorAll("[data-add-cart]").forEach((button) => {
  button.addEventListener("click", () => {
    cartItems += 1;
    if (cartCount) cartCount.textContent = String(cartItems);
    showToast("Added to your private cart");
  });
});

document.querySelectorAll(".product-image img").forEach((image) => {
  image.addEventListener("error", () => {
    image.src = fallbackImage(image.alt);
    image.classList.add("is-fallback");
  }, { once: true });
});

const revealItems = document.querySelectorAll(
  ".product-card, .section-heading, .editorial-band, .site-footer, .page-hero, .product-detail"
);

if ("IntersectionObserver" in window) {
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.16 });

  revealItems.forEach((item, index) => {
    item.style.transitionDelay = `${Math.min(index % 9, 8) * 55}ms`;
    revealObserver.observe(item);
  });
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

document.querySelectorAll(".product-card").forEach((card) => {
  card.addEventListener("mousemove", (event) => {
    const bounds = card.getBoundingClientRect();
    const x = ((event.clientX - bounds.left) / bounds.width - 0.5) * 6;
    const y = ((event.clientY - bounds.top) / bounds.height - 0.5) * -6;
    card.style.transform = `perspective(900px) rotateX(${y}deg) rotateY(${x}deg)`;
  });
  card.addEventListener("mouseleave", () => {
    card.style.transform = "";
  });
});

const chatbotContainer = document.querySelector(".chatbot");
const chatOpen = document.querySelector("[data-chatbot-open]");
const chatClose = document.querySelector("[data-chatbot-close]");
const chatPanel = document.querySelector("[data-chatbot-panel]");
const chatBody = document.querySelector("[data-chatbot-body]");
const chatForm = document.querySelector("[data-chatbot-form]");
const chatInput = document.querySelector("#chatbot-input");

function createChatMessage(text, role, html = false) {
  const message = document.createElement("div");
  message.className = `chatbot-message ${role}`;
  if (html) {
    message.innerHTML = text;
  } else {
    const paragraph = document.createElement("p");
    paragraph.textContent = text;
    message.appendChild(paragraph);
  }
  return message;
}

function scrollChatToBottom() {
  if (chatBody) {
    chatBody.scrollTop = chatBody.scrollHeight;
  }
}

function setChatPanelOpen(open) {
  if (!chatbotContainer || !chatOpen || !chatPanel) return;
  chatbotContainer.classList.toggle("is-open", open);
  chatOpen.setAttribute("aria-expanded", String(open));
  if (open) {
    chatPanel.removeAttribute("hidden");
    chatInput?.focus();
    scrollChatToBottom();
  } else {
    chatPanel.setAttribute("hidden", "true");
  }
}

if (chatOpen && chatClose && chatbotContainer) {
  chatOpen.addEventListener("click", () => {
    const isOpen = chatbotContainer.classList.contains("is-open");
    setChatPanelOpen(!isOpen);
  });
  chatClose.addEventListener("click", () => setChatPanelOpen(false));
}

async function askBot(question) {
  if (!question || !chatBody) return;
  chatBody.appendChild(createChatMessage(question, "customer"));
  scrollChatToBottom();
  chatInput.value = "";

  const placeholder = createChatMessage("Thinking...", "assistant");
  chatBody.appendChild(placeholder);
  scrollChatToBottom();

  try {
    const encoded = encodeURIComponent(question);
    const response = await fetch(`/chatbot/response/?message=${encoded}`);
    const data = await response.json();
    placeholder.remove();
    if (data.reply_html) {
      chatBody.appendChild(createChatMessage(data.reply_html, "assistant", true));
    } else {
      chatBody.appendChild(createChatMessage(data.reply || "Sorry, I couldn't find that. Try asking about cooling, shipping, GPUs, cabinets, or prebuilt PCs.", "assistant"));
    }
    scrollChatToBottom();
  } catch (error) {
    placeholder.remove();
    chatBody.appendChild(createChatMessage("There was a problem connecting to the chatbot. Please try again.", "assistant"));
    scrollChatToBottom();
  }
}

if (chatForm) {
  chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = chatInput?.value.trim();
    if (text) askBot(text);
  });
}
