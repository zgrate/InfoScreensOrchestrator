# Edit this configuration file to define what should be installed on
# your system.  Help is available in the configuration.nix(5) man page
# and in the NixOS manual (accessible by running `nixos-help`).

{ config, pkgs, ... }:

let 
    HOSTNAME = "kiosk-wyse-1";
    SCREEN_IP = "http://192.168.16.20:8000/";
    SCREEN_PASSPHRASE = "lobby123";
    ZERO_TIER_NETWORK = "e5cd7a9e1c094dca";

    screenPythonEnv = pkgs.buildEnv {
      name = "screen-python-envs";
      paths = [
        (pkgs.python311.withPackages(ps: with ps; [requests]))  # Use the Python 3.11 interpreter installed as a system package
      ];
    };
in
{
  imports =
    [ # Include the results of the hardware scan.
      ./hardware-configuration.nix
    ];

  environment.sessionVariables = {
    SCREEN_IP = SCREEN_IP;
    SCREEN_PASSPHRASE = SCREEN_PASSPHRASE;
  };


  networking.wireless.networks =
  {
    "Hausmeerschweichen" = {
       psk = "1234567890abcde";
    };

    "Hotel Ameliowka" = {};
    
    "Kawiarnia Ameliowka" = {
      psk = "0123456789";
    };
  };

#  services.cage.program = "${pkgs.firefox}/bin/firefox -kiosk http://screen.futerkon.pl/";

  services.cage.program = "${screenPythonEnv}/bin/python /usr/script.py";


   users.users.kiosk = {
    isNormalUser = true;
    description = "Kioks user";
    extraGroups = [ "wheel" ];
    hashedPassword = "$6$fDenph8Oybmp0rNk$fD1F4K6fmmEKEfIxdkS5896HewGUjYeBxdYfJjbnv7Pf0Huat10y2sE8LU3bD5a/06euYjWaZWaKRK3bTriI01";
    uid = 1000;
  };


  boot.plymouth.enable = true;
  boot.plymouth.logo = pkgs.fetchurl {
          url = "https://storage.zgrate.ovh/znerd-small.png";
          sha256 = "e8a692068c9ce6ccfe40186ca0e0096d966205b70f413c309ff8051e98e2592e";
        };


  environment.systemPackages = with pkgs; [
    vim # Do not forget to add an editor to edit configuration.nix! The Nano editor is also installed by default.
    wget
    mpv
    firefox
    socat
    python311
    git
    htop
  ];


    # Use the systemd-boot EFI boot loader.
  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  networking.hostName = HOSTNAME; # Define your hostname.
  # Pick only one of the below networking options.
  networking.wireless.enable = true;  # Enables wireless support via wpa_supplicant.
  #networking.networkmanager.enable = true;  # Easiest to use and most distros use this by default.



  # Set your time zone.
  time.timeZone = "Europe/Warsaw";

  # Configure network proxy if necessary
  # networking.proxy.default = "http://user:password@proxy:port/";
  # networking.proxy.noProxy = "127.0.0.1,localhost,internal.domain";

  # Select internationalisation properties.
  # i18n.defaultLocale = "en_US.UTF-8";
  # console = {
  #   font = "Lat2-Terminus16";
  #   keyMap = "us";
  #   useXkbConfig = true; # use xkbOptions in tty.
  # };

  # Enable the X11 windowing system.
  # services.xserver.enable = true;


  nixpkgs.config.allowUnfree = true;

  nixpkgs.config.packageOverrides = pkgs: {
    vaapiIntel = pkgs.vaapiIntel.override { enableHybridCodec = true; };
  };

  hardware.opengl = {
    enable = true;
    extraPackages = with pkgs; [
      intel-media-driver
      vaapiIntel
      vaapiVdpau
      libvdpau-va-gl
    ];
  };

  services.zerotierone.enable = true;
  services.zerotierone.joinNetworks = [ZERO_TIER_NETWORK];


  services.cage.enable = true;
  services.cage.user = "kiosk";

  # Configure keymap in X11
  # services.xserver.layout = "us";
  # services.xserver.xkbOptions = "eurosign:e,caps:escape";

  # Enable CUPS to print documents.
  # services.printing.enable = true;

  # Enable sound.
  sound.enable = true;
  hardware.pulseaudio.enable = true;

  nixpkgs.config.pulseaudio = true;

  # Enable touchpad support (enabled default in most desktopManager).
  # services.xserver.libinput.enable = true;


  security.polkit.extraConfig = '' 
    polkit.addRule(function(action, subject) {
      if (subject.isInGroup("wheel")) {
        return polkit.Result.YES;
      }
    });
  '';

  security.sudo = {
    enable = true;
    wheelNeedsPassword = false;
  };

  
  # List packages installed in system profile. To search, run:
  # $ nix search wget
  
  # Some programs need SUID wrappers, can be configured further or are
  # started in user sessions.
  # programs.mtr.enable = true;
  # programs.gnupg.agent = {
  #   enable = true;
  #   enableSSHSupport = true;
  # };

  # List services that you want to enable:

  # Enable the OpenSSH daemon.
  services.openssh.enable = true;

  networking.dhcpcd.wait = "if-carrier-up";

  systemd.network.wait-online.anyInterface = true;

  # Open ports in the firewall.
  # networking.firewall.allowedTCPPorts = [ ... ];
  # networking.firewall.allowedUDPPorts = [ ... ];
  # Or disable the firewall altogether.
  # networking.firewall.enable = false;

  # Copy the NixOS configuration file and link it from the resulting system
  # (/run/current-system/configuration.nix). This is useful in case you
  # accidentally delete configuration.nix.
  system.copySystemConfiguration = true;

  # This value determines the NixOS release from which the default
  # settings for stateful data, like file locations and database versions
  # on your system were taken. It's perfectly fine and recommended to leave
  # this value at the release version of the first install of this system.
  # Before changing this value read the documentation for this option
  # (e.g. man configuration.nix or on https://nixos.org/nixos/options.html).
  system.stateVersion = "23.05"; # Did you read the comment?

}
