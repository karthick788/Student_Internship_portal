async function finishGoogleSignIn(credential) {
  showBusy("Signing in with Google...");
  try {
    const data = await API.apiRequest("/auth/google", {
      method: "POST",
      body: JSON.stringify({ credential }),
    });
    if (!data?.token) throw new Error("Google sign-in did not return a session.");
    API.setSession(data.token, data.student);
    const needsProfile = data.needs_profile || !data.student?.phone || !data.student?.college;
    showToast(needsProfile ? "Add your profile details to continue" : "Signed in with Google", "success");
    const inPages = window.location.pathname.includes("/pages/");
    const dest = needsProfile ? "profile.html" : "dashboard.html";
    window.location.href = inPages ? dest : `pages/${dest}`;
  } catch (err) {
    hideBusy();
    showToast(err.message, "error");
  }
}

async function mountGoogleButton(containerId) {
  const wrap = document.getElementById(containerId);
  if (!wrap) return;
  let config;
  try {
    config = await API.apiRequest("/auth/config");
  } catch {
    wrap.innerHTML = `<p class="google-hint">Could not load Google sign-in.</p>`;
    return;
  }
  if (!config?.google_client_id) {
    wrap.innerHTML = `<p class="google-hint">Add GOOGLE_CLIENT_ID in server/.env to enable Google login.</p>`;
    return;
  }

  await new Promise((resolve, reject) => {
    if (window.google?.accounts?.id) return resolve();
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });

  window.google.accounts.id.initialize({
    client_id: config.google_client_id,
    callback: (response) => finishGoogleSignIn(response.credential),
  });
  wrap.innerHTML = "";
  window.google.accounts.id.renderButton(wrap, {
    theme: "outline",
    size: "large",
    text: "continue_with",
    width: 320,
  });
}
