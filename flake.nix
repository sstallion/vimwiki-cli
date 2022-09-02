{
  description = "Fork of vimwiki-cli so I can bump the deps lol";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
  };

  outputs = { self, nixpkgs }:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
      my-python = pkgs.python3;
      python-with-my-packages = my-python.withPackages (p: with p; [
        click
      ]);
      python-deps = with pkgs.python3Packages; [
        click
        setuptools
      ];
    in
    {
      packages.x86_64-linux.vimwiki-cli = pkgs.python3Packages.buildPythonPackage {
        pname = "vimwiki-cli";
        src = ./.;
        version = "1.0.0";
        bulidInputs = [ python-deps  ];
        propagatedBuildInputs = [ python-deps ];
        doCheck = false;
      };
      packages.x86_64-linux.defaultPackage.x86_64-linux = self.packages.x86_64-linux.vimwiki-cli;
      devShell.x86_64-linux = pkgs.mkShell {
        buildInputs = [
          python-with-my-packages
          self.packages.x86_64-linux.vimwiki-cli
        ];
      };
    };
}
