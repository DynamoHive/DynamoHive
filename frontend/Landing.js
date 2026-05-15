   <a
            href="/legal.html"
            style={footerLink}
          >
            Legal
          </a>

          <a
            href="/privacy.html"
            style={footerLink}
          >
            Privacy
          </a>

        </div>

      </footer>

    </div>
  );
}


function FeatureCard({ title, text }) {

  return (

    <div
      style={{
        background: "#12121A",
        border: "1px solid #1F2937",
        borderRadius: "18px",
        padding: "28px"
      }}
    >

      <h3
        style={{
          marginBottom: "14px"
        }}
      >
        {title}
      </h3>

      <p
        style={{
          color: "#9CA3AF",
          lineHeight: "1.6"
        }}
      >
        {text}
      </p>

    </div>
  );
}


function StatusItem({ label, value }) {

  return (

    <div>

      <div
        style={{
          color: "#777",
          marginBottom: "8px",
          fontSize: "14px"
        }}
      >
        {label}
      </div>

      <div
        style={{
          color: "#00D1FF",
          fontWeight: "bold"
        }}
      >
        {value}
      </div>

    </div>
  );
}


const footerLink = {
  color: "#666",
  textDecoration: "none",
  marginLeft: "20px"
};
