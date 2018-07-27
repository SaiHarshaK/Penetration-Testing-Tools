#!/usr/bin/perl
# Alternative to grep Unix command.


$opt = shift;
if ($opt =~ s/^\-//) {
  $re = shift;
} else {
  $re = $opt;
  $opt = "";
}
die "Usage: grep.pl [-iv] regexp [files]\n" if ! defined $re;
$igncase = ($opt =~ s/i//g);
$nomatch = ($opt =~ s/v//g);
die "Unknown option `$opt'\n" if $opt ne "";
@ARGV = ("-") if $#ARGV < 0;
for $fn1 (@ARGV) {
 for $fn (glob $fn1) {
  if (open FH, "<$fn") {
    $pref = $fn eq "-" ? "" : "$fn:";
    if ($igncase) {
      while (<FH>) {
        print  "$pref$.:$_" if (/$re/i) xor $nomatch;
      }
    } else {
      while (<FH>) {
        print  "$pref$.:$_" if (/$re/) xor $nomatch;
      }
    }
    close FH;
  }