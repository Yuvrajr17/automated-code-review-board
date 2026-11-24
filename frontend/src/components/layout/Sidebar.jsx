
const navigationItems = [
  { label: "Dashboard", icon: "▦", active: true },
  { label: "Review History", icon: "◷", active: false },
];

function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 flex-col bg-[#191D23] text-slate-300 md:flex">
      {/* Brand */}
      <div className="flex h-16 items-center border-b border-white/10 px-6">
        <div className="mr-3 flex h-8 w-8 items-center justify-center rounded bg-emerald-700 font-bold text-white">
          CR
        </div>
        <span className="font-semibold tracking-tight text-white">
          ReviewBoard
        </span>
      </div>

      {/* Navigation */}
      <div className="px-4 py-6">
        <p className="mb-3 px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
          Workspace
        </p>

        <nav className="space-y-1">
          {navigationItems.map((item) => (
            <a
              key={item.label}
              href="#"
              className={`flex items-center rounded-md px-3 py-2.5 text-sm transition ${
                item.active
                  ? "bg-white/10 font-medium text-white"
                  : "text-slate-400 hover:bg-white/5 hover:text-white"
              }`}
            >
              <span className="mr-3 text-base">{item.icon}</span>
              {item.label}
            </a>
          ))}
        </nav>

        <p className="mb-3 mt-9 px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
          Preferences
        </p>

        <a
          href="#"
          className="flex items-center rounded-md px-3 py-2.5 text-sm text-slate-400 transition hover:bg-white/5 hover:text-white"
        >
          <span className="mr-3 text-base">⚙</span>
          Settings
        </a>
      </div>

      {/* Footer */}
      <div className="mt-auto border-t border-white/10 p-5">
        <p className="text-xs text-slate-500">Multi-Agent System</p>
        <p className="mt-1 text-sm font-medium text-slate-300">
          Phase 1 · Local Workspace
        </p>
      </div>
    </aside>
  );
}

export default Sidebar;
