{
  description = "GTK4 native deps for uv-managed Python";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          gcc
          pkg-config

          glib
          gobject-introspection
          gsettings-desktop-schemas

          gtk4
          cairo
          pango
          graphene
          gdk-pixbuf
          libadwaita
        ];

        env = {
          GI_TYPELIB_PATH = pkgs.lib.makeSearchPath "lib/girepository-1.0" [
            pkgs.gobject-introspection
            pkgs.glib
            pkgs.gtk4
            pkgs.pango
            pkgs.graphene
            pkgs.gdk-pixbuf
            pkgs.libadwaita
          ];

          XDG_DATA_DIRS = pkgs.lib.makeSearchPath "share" [
            pkgs.gtk4
            pkgs.libadwaita
            pkgs.gsettings-desktop-schemas
          ];

          GSETTINGS_SCHEMA_DIR = "${pkgs.gsettings-desktop-schemas}/share/gsettings-schemas/${pkgs.gsettings-desktop-schemas.name}";
        };
      };
    };
}
