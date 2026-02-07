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

          gtk4
          cairo
          pango
          graphene
          gdk-pixbuf
        ];

        env = {
          GI_TYPELIB_PATH = pkgs.lib.makeSearchPath "lib/girepository-1.0" [
            pkgs.gobject-introspection
            pkgs.glib
            pkgs.gtk4
            pkgs.pango
            pkgs.graphene
            pkgs.gdk-pixbuf
          ];
        };
      };
    };
}
